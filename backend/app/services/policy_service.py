from copy import deepcopy

from app.repositories.budget_policy_repository import BudgetPolicyRepository
from app.repositories.governance_policy_repository import GovernancePolicyRepository
from app.repositories.policy_version_repository import PolicyVersionRepository
from app.services.policy_deployment_service import PolicyDeploymentService
from app.services.policy_rego_generator import PolicyRegoGenerator


class PolicyService:
    DECISIONS = ["ALLOW", "DENY", "REQUIRE_APPROVAL"]
    STATUSES = ["ACTIVE", "INACTIVE", "MAINTENANCE", "DELETED"]
    BUDGET_STATUSES = ["ACTIVE", "INACTIVE"]
    DEPARTMENTS = ["Finance", "HR", "Sales", "Operations", "IT"]

    def __init__(
        self,
        opa_adapter,
        governance_repository: GovernancePolicyRepository,
        budget_repository: BudgetPolicyRepository,
        version_repository: PolicyVersionRepository,
        deployment_service: PolicyDeploymentService,
    ):
        self.opa_adapter = opa_adapter
        self.governance_repository = governance_repository
        self.budget_repository = budget_repository
        self.version_repository = version_repository
        self.deployment_service = deployment_service
        self.rego_generator = PolicyRegoGenerator()

    def list_policies(self) -> list:
        return self.governance_repository.list_ordered()

    def list_governance_policies(self) -> list:
        return self.governance_repository.list_ordered()

    def get_governance_policy(self, policy_id: int):
        return self.governance_repository.get(policy_id)

    def create_governance_policy(self, payload) -> object:
        data = self._governance_data(payload)
        self._validate_governance_policy(data)
        if self.governance_repository.get_by_policy_id(data["policy_id"]):
            raise ValueError(f"Policy ID '{data['policy_id']}' already exists")
        policy = self.governance_repository.create(data)
        self.deployment_service.deploy("CREATE_GOVERNANCE_POLICY")
        return policy

    def update_governance_policy(self, policy, payload) -> object:
        data = self._governance_data(payload, exclude_unset=True)
        candidate = {**self._governance_data(policy), **data}
        self._validate_governance_policy(candidate)
        if data.get("policy_id"):
            existing = self.governance_repository.get_by_policy_id(data["policy_id"])
            if existing and existing.id != policy.id:
                raise ValueError(f"Policy ID '{data['policy_id']}' already exists")
        updated = self.governance_repository.update(policy, data)
        self.deployment_service.deploy("UPDATE_GOVERNANCE_POLICY")
        return updated

    def delete_governance_policy(self, policy) -> None:
        self.governance_repository.delete(policy)
        self.deployment_service.deploy("DELETE_GOVERNANCE_POLICY")

    def duplicate_governance_policy(self, policy) -> object:
        data = self._governance_data(policy)
        data["policy_id"] = self._copy_key(data["policy_id"], self.governance_repository.get_by_policy_id)
        data["name"] = f"{data['name']} Copy"
        duplicate = self.governance_repository.create(data)
        self.deployment_service.deploy("DUPLICATE_GOVERNANCE_POLICY")
        return duplicate

    def set_governance_enabled(self, policy, enabled: bool) -> object:
        updated = self.governance_repository.update(policy, {"enabled": enabled})
        self.deployment_service.deploy("SET_GOVERNANCE_POLICY_ENABLED")
        return updated

    def list_budget_policies(self) -> list:
        return self.budget_repository.list_ordered()

    def get_budget_policy(self, policy_id: int):
        return self.budget_repository.get(policy_id)

    def create_budget_policy(self, payload) -> object:
        data = self._budget_data(payload)
        self._validate_budget_policy(data)
        if self.budget_repository.get_by_name(data["name"]):
            raise ValueError(f"Budget policy '{data['name']}' already exists")
        policy = self.budget_repository.create(data)
        self.deployment_service.deploy("CREATE_BUDGET_POLICY")
        return policy

    def update_budget_policy(self, policy, payload) -> object:
        data = self._budget_data(payload, exclude_unset=True)
        candidate = {**self._budget_data(policy), **data}
        self._validate_budget_policy(candidate)
        if data.get("name"):
            existing = self.budget_repository.get_by_name(data["name"])
            if existing and existing.id != policy.id:
                raise ValueError(f"Budget policy '{data['name']}' already exists")
        updated = self.budget_repository.update(policy, data)
        self.deployment_service.deploy("UPDATE_BUDGET_POLICY")
        return updated

    def delete_budget_policy(self, policy) -> None:
        self.budget_repository.delete(policy)
        self.deployment_service.deploy("DELETE_BUDGET_POLICY")

    def duplicate_budget_policy(self, policy) -> object:
        data = self._budget_data(policy)
        data["name"] = self._copy_key(data["name"], self.budget_repository.get_by_name)
        duplicate = self.budget_repository.create(data)
        self.deployment_service.deploy("DUPLICATE_BUDGET_POLICY")
        return duplicate

    def set_budget_status(self, policy, status: str) -> object:
        if status not in self.BUDGET_STATUSES:
            raise ValueError(f"Unsupported budget policy status: {status}")
        updated = self.budget_repository.update(policy, {"status": status})
        self.deployment_service.deploy("SET_BUDGET_POLICY_STATUS")
        return updated

    def latest_deployment(self):
        return self.deployment_service.latest()

    def deploy(self):
        return self.deployment_service.deploy("MANUAL_DEPLOY")

    def history(self) -> list:
        return self.version_repository.list_recent()

    def compare_versions(self, left_id: str, right_id: str) -> dict:
        left = self.version_repository.get_by_version_id(left_id)
        right = self.version_repository.get_by_version_id(right_id)
        if not left or not right:
            raise ValueError("Both policy versions must exist")
        summary = []
        if left.generated_rego != right.generated_rego:
            summary.append("Generated Rego changed")
        if left.snapshot != right.snapshot:
            summary.append("JSON policy snapshot changed")
        return {"left": left, "right": right, "changed": bool(summary), "summary": summary or ["No differences detected"]}

    def restore_version(self, version_id: str):
        version = self.version_repository.get_by_version_id(version_id)
        if not version:
            raise ValueError("Policy version not found")
        snapshot = version.snapshot or {}
        for policy in self.governance_repository.list(0, 1000):
            self.governance_repository.delete(policy)
        for policy in self.budget_repository.list(0, 1000):
            self.budget_repository.delete(policy)
        for policy_data in snapshot.get("governance_policies", []):
            self.governance_repository.create(policy_data)
        for budget_data in snapshot.get("budget_policies", []):
            self.budget_repository.create(budget_data)
        return self.deployment_service.deploy("RESTORE_POLICY_VERSION")

    def count_active(self) -> int:
        return len(self.governance_repository.list_active()) + len(self.budget_repository.list_active())

    def lookups(self) -> dict:
        return {
            "decisions": self.DECISIONS,
            "statuses": self.STATUSES,
            "budget_statuses": self.BUDGET_STATUSES,
            "departments": self.DEPARTMENTS,
            "condition_fields": [{"value": key, "label": key.replace(".", " / ")} for key in self.rego_generator.CONDITION_FIELDS],
            "condition_operators": [
                {"value": "equals", "label": "Equals"},
                {"value": "not_equals", "label": "Does Not Equal"},
                {"value": "greater_than", "label": "Greater Than"},
                {"value": "greater_or_equal", "label": "Greater Or Equal"},
                {"value": "less_than", "label": "Less Than"},
                {"value": "less_or_equal", "label": "Less Or Equal"},
                {"value": "contains", "label": "Contains"},
            ],
        }

    def evaluate(self, identity: dict, normalized_execution: dict, risk: dict) -> dict:
        result = self.opa_adapter.evaluate(self._build_opa_input(identity, normalized_execution, risk))
        return {
            "decision": result.decision,
            "matched_policy": result.matched_policy,
            "reasons": result.reasons,
            "opa_url": result.opa_url,
            "raw_result": result.raw_result,
        }

    def _validate_governance_policy(self, data: dict) -> None:
        if data["decision"] not in self.DECISIONS:
            raise ValueError(f"Unsupported policy decision: {data['decision']}")
        for condition in data.get("conditions", []):
            if condition.get("field") not in self.rego_generator.CONDITION_FIELDS:
                raise ValueError(f"Unsupported condition field: {condition.get('field')}")
            operator = condition.get("operator")
            if operator != "contains" and operator not in self.rego_generator.OPERATORS:
                raise ValueError(f"Unsupported condition operator: {operator}")

    def _validate_budget_policy(self, data: dict) -> None:
        if data["department"] not in self.DEPARTMENTS:
            raise ValueError(f"Unsupported department: {data['department']}")
        if data["status"] not in self.BUDGET_STATUSES:
            raise ValueError(f"Unsupported budget policy status: {data['status']}")
        if data["approval_threshold"] > data["transaction_limit"]:
            raise ValueError("Approval threshold cannot exceed transaction limit")

    def _governance_data(self, source, exclude_unset: bool = False) -> dict:
        data = self._model_dump(source, exclude_unset)
        if "conditions" in data:
            data["conditions"] = [self._model_dump(condition) for condition in data["conditions"]]
        return data

    def _budget_data(self, source, exclude_unset: bool = False) -> dict:
        return self._model_dump(source, exclude_unset)

    def _model_dump(self, source, exclude_unset: bool = False) -> dict:
        if hasattr(source, "model_dump"):
            return source.model_dump(exclude_unset=exclude_unset)
        fields = [
            "policy_id",
            "name",
            "description",
            "decision",
            "priority",
            "enabled",
            "conditions",
            "reason",
            "department",
            "daily_limit",
            "monthly_limit",
            "transaction_limit",
            "approval_threshold",
            "spent_today",
            "spent_month",
            "status",
        ]
        return {field: deepcopy(getattr(source, field)) for field in fields if hasattr(source, field)}

    def _copy_key(self, base_key: str, exists) -> str:
        candidate = f"{base_key}_copy"
        index = 2
        while exists(candidate):
            candidate = f"{base_key}_copy_{index}"
            index += 1
        return candidate

    def _build_opa_input(self, identity: dict, normalized_execution: dict, risk: dict) -> dict:
        parameters = normalized_execution.get("parameters", {})
        return {
            "identity": {
                "passportId": identity.get("passport_id"),
                "agentName": identity.get("agent_name"),
                "department": identity.get("department"),
                "owner": identity.get("owner"),
                "status": identity.get("status"),
                "trustScore": identity.get("trust_score"),
                "reputation": identity.get("reputation"),
                "riskTier": identity.get("risk_tier"),
                "allowedApis": identity.get("allowed_apis", []),
                "allowedOperations": identity.get("allowed_operations", []),
                "policyGroups": identity.get("policy_groups", []),
                "budgetProfile": identity.get("budget_profile"),
            },
            "normalizedExecution": {
                "service": normalized_execution.get("service"),
                "operation": normalized_execution.get("operation"),
                "parameters": parameters,
                "parameterText": str(parameters),
                "amount": float(normalized_execution.get("amount") or 0),
            },
            "risk": risk,
        }
