import hashlib
import shutil
import subprocess
from pathlib import Path
from uuid import uuid4

from app.models.policy_deployment import PolicyDeployment
from app.repositories.budget_policy_repository import BudgetPolicyRepository
from app.repositories.governance_policy_repository import GovernancePolicyRepository
from app.repositories.policy_deployment_repository import PolicyDeploymentRepository
from app.repositories.policy_version_repository import PolicyVersionRepository
from app.services.policy_rego_generator import PolicyRegoGenerator


class PolicyDeploymentService:
    def __init__(
        self,
        governance_repository: GovernancePolicyRepository,
        budget_repository: BudgetPolicyRepository,
        version_repository: PolicyVersionRepository,
        deployment_repository: PolicyDeploymentRepository,
        policy_directory: str,
        opa_cli_path: str = "opa",
    ):
        self.governance_repository = governance_repository
        self.budget_repository = budget_repository
        self.version_repository = version_repository
        self.deployment_repository = deployment_repository
        self.policy_directory = Path(policy_directory)
        self.opa_cli_path = opa_cli_path
        self.generator = PolicyRegoGenerator()

    def deploy(self, action: str = "DEPLOY") -> PolicyDeployment:
        policies = self.governance_repository.list_ordered()
        budgets = self.budget_repository.list_ordered()
        generated_rego = self.generator.render(policies, budgets)
        self.policy_directory.mkdir(parents=True, exist_ok=True)
        target = self.policy_directory / "governance.rego"
        draft = self.policy_directory / "governance.rego.tmp"
        draft.write_text(generated_rego, encoding="utf-8")

        if self._opa_cli_available():
            fmt_status, fmt_message = self._run_opa(["fmt", "-w", str(draft)])
            check_status, check_message = self._run_opa(["check", str(draft)])
        else:
            fmt_status, fmt_message = self._run_internal_fmt(draft)
            check_status, check_message = self._run_internal_check(draft)

        if fmt_status == "PASSED" and check_status == "PASSED":
            generated_rego = draft.read_text(encoding="utf-8")
            checksum = hashlib.sha256(generated_rego.encode("utf-8")).hexdigest()
            shutil.move(str(draft), str(target))
            status = "DEPLOYED"
            message = self._deployment_message(fmt_message, check_message)
            reload_status = "OPA_RESTARTED"
            from app.core.opa_runner import restart_opa_server
            restart_opa_server(opa_cli_path=self.opa_cli_path, bundle_path=str(self.policy_directory))
        else:
            checksum = hashlib.sha256(generated_rego.encode("utf-8")).hexdigest()
            draft.unlink(missing_ok=True)
            status = "FAILED"
            message = " ".join(part for part in [fmt_message, check_message] if part) or "OPA validation failed."
            reload_status = "NOT_RUN"

        deployment = self.deployment_repository.create(
            {
                "deployment_id": f"DEP-{uuid4().hex[:10].upper()}",
                "status": status,
                "message": message,
                "checksum": checksum,
                "opa_fmt_status": fmt_status,
                "opa_check_status": check_status,
                "opa_reload_status": reload_status,
            }
        )
        self.version_repository.create(
            {
                "version_id": f"POLVER-{uuid4().hex[:10].upper()}",
                "resource_type": "bundle",
                "resource_key": "governance.rego",
                "action": action,
                "snapshot": {
                    "governance_policies": [self._governance_snapshot(policy) for policy in policies],
                    "budget_policies": [self._budget_snapshot(policy) for policy in budgets],
                },
                "generated_rego": generated_rego,
            }
        )
        self.deployment_repository.db.commit()
        return deployment

    def latest(self) -> PolicyDeployment | None:
        return self.deployment_repository.latest()

    def _run_opa(self, command: list[str]) -> tuple[str, str]:
        executable = self._resolve_opa_cli()
        if executable is None:
            return "FAILED", "OPA CLI was not found on PATH."
        try:
            result = subprocess.run([executable, *command], check=False, capture_output=True, text=True, timeout=10)
        except FileNotFoundError:
            return "FAILED", "OPA CLI was not found on PATH."
        except subprocess.TimeoutExpired:
            return "FAILED", "OPA command timed out."
        if result.returncode == 0:
            return "PASSED", result.stdout.strip()
        return "FAILED", (result.stderr or result.stdout).strip()

    def _opa_cli_available(self) -> bool:
        return self._resolve_opa_cli() is not None

    def _resolve_opa_cli(self) -> str | None:
        configured = Path(self.opa_cli_path)
        if configured.exists():
            return str(configured)
        return shutil.which(self.opa_cli_path)

    def _run_internal_fmt(self, draft: Path) -> tuple[str, str]:
        text = draft.read_text(encoding="utf-8").strip() + "\n"
        draft.write_text(text, encoding="utf-8")
        return "PASSED", "OPA CLI not found; used SentinelAI generated-Rego formatter fallback."

    def _run_internal_check(self, draft: Path) -> tuple[str, str]:
        rego = draft.read_text(encoding="utf-8")
        missing = [token for token in ["package sentinelai.governance", "default decision :=", "decision := result if"] if token not in rego]
        if missing:
            return "FAILED", f"Generated Rego failed internal check; missing {', '.join(missing)}."
        bracket_error = self._balanced_brackets_error(rego)
        if bracket_error:
            return "FAILED", bracket_error
        return "PASSED", "OPA CLI not found; internal Rego structure check passed. Install OPA CLI for external opa check."

    def _balanced_brackets_error(self, rego: str) -> str:
        pairs = {"}": "{", "]": "[", ")": "("}
        stack: list[str] = []
        in_string = False
        escaped = False
        for character in rego:
            if in_string:
                if escaped:
                    escaped = False
                elif character == "\\":
                    escaped = True
                elif character == '"':
                    in_string = False
                continue
            if character == '"':
                in_string = True
                continue
            if character in "{[(":
                stack.append(character)
            elif character in pairs:
                if not stack or stack.pop() != pairs[character]:
                    return "Generated Rego failed internal check; bracket structure is invalid."
        if in_string:
            return "Generated Rego failed internal check; string literal is incomplete."
        if stack:
            return "Generated Rego failed internal check; bracket structure is incomplete."
        return ""

    def _deployment_message(self, fmt_message: str, check_message: str) -> str:
        fallback_used = "OPA CLI not found" in f"{fmt_message} {check_message}"
        if fallback_used:
            return "governance.rego generated and deployed with SentinelAI internal formatter/check because OPA CLI was not found on PATH."
        return "governance.rego generated, formatted, checked, and written for OPA watch reload."

    def _governance_snapshot(self, policy) -> dict:
        return {
            "policy_id": policy.policy_id,
            "name": policy.name,
            "description": policy.description,
            "decision": policy.decision,
            "priority": policy.priority,
            "enabled": policy.enabled,
            "conditions": policy.conditions,
            "reason": policy.reason,
        }

    def _budget_snapshot(self, policy) -> dict:
        return {
            "name": policy.name,
            "department": policy.department,
            "daily_limit": policy.daily_limit,
            "monthly_limit": policy.monthly_limit,
            "transaction_limit": policy.transaction_limit,
            "approval_threshold": policy.approval_threshold,
            "spent_today": policy.spent_today,
            "spent_month": policy.spent_month,
            "status": policy.status,
        }
