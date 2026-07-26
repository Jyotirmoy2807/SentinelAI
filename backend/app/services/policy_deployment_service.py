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
    ):
        self.governance_repository = governance_repository
        self.budget_repository = budget_repository
        self.version_repository = version_repository
        self.deployment_repository = deployment_repository
        self.policy_directory = Path(policy_directory)
        self.generator = PolicyRegoGenerator()

    def deploy(self, action: str = "DEPLOY") -> PolicyDeployment:
        policies = self.governance_repository.list_ordered()
        budgets = self.budget_repository.list_ordered()
        generated_rego = self.generator.render(policies, budgets)
        checksum = hashlib.sha256(generated_rego.encode("utf-8")).hexdigest()
        self.policy_directory.mkdir(parents=True, exist_ok=True)
        target = self.policy_directory / "governance.rego"
        draft = self.policy_directory / "governance.rego.tmp"
        draft.write_text(generated_rego, encoding="utf-8")

        fmt_status, fmt_message = self._run_opa(["opa", "fmt", "-w", str(draft)])
        check_status, check_message = self._run_opa(["opa", "check", str(draft)])
        if fmt_status == "PASSED" and check_status == "PASSED":
            shutil.move(str(draft), str(target))
            status = "DEPLOYED"
            message = "governance.rego generated, formatted, checked, and written for OPA watch reload."
            reload_status = "WATCHED_FILE_REPLACED"
        else:
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
        try:
            result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=10)
        except FileNotFoundError:
            return "FAILED", "OPA CLI was not found on PATH."
        except subprocess.TimeoutExpired:
            return "FAILED", "OPA command timed out."
        if result.returncode == 0:
            return "PASSED", result.stdout.strip()
        return "FAILED", (result.stderr or result.stdout).strip()

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
