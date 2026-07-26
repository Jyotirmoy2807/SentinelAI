from typing import Any

from app.models.policy import Policy
from app.repositories.policy_repository import PolicyRepository


class PolicyService:
    def __init__(self, repository: PolicyRepository):
        self.repository = repository

    def list_policies(self) -> list[Policy]:
        return self.repository.list()

    def get_policy(self, policy_id: int) -> Policy | None:
        return self.repository.get(policy_id)

    def create_policy(self, data: dict) -> Policy:
        policy = self.repository.create(data)
        self.repository.db.commit()
        return policy

    def update_policy(self, policy: Policy, data: dict) -> Policy:
        updated = self.repository.update(policy, data)
        self.repository.db.commit()
        return updated

    def delete_policy(self, policy: Policy) -> Policy:
        updated = self.repository.update(policy, {"status": "DELETED"})
        self.repository.db.commit()
        return updated

    def evaluate(self, identity: dict, normalized_execution: dict) -> dict:
        service = normalized_execution.get("service")
        operation = normalized_execution.get("operation")
        amount = normalized_execution.get("amount", 0)
        allowed_apis = identity.get("allowed_apis", [])
        allowed_operations = identity.get("allowed_operations", [])

        violations: list[dict[str, Any]] = []
        matched: list[dict[str, Any]] = []
        approval_reasons: list[str] = []

        if service not in allowed_apis:
            violations.append({"type": "SERVICE_NOT_ALLOWED", "message": f"{service} is not in Agent Passport allowed APIs."})
        if operation not in allowed_operations:
            violations.append(
                {"type": "OPERATION_NOT_ALLOWED", "message": f"{operation} is not in Agent Passport allowed operations."}
            )
        if violations:
            return {
                "decision": "DENY",
                "matching_policies": matched,
                "violated_policies": violations,
                "missing_permissions": [item["type"] for item in violations],
                "reasons": [item["message"] for item in violations],
            }

        for policy in self.repository.list_active():
            if not self._policy_group_applies(policy, identity):
                continue
            if not self._conditions_match(policy.conditions or {}, identity, normalized_execution):
                continue
            policy_record = {
                "policy_id": policy.policy_id,
                "name": policy.name,
                "priority": policy.priority,
                "version": policy.version,
                "decision": policy.actions.get("decision", "ALLOW"),
            }
            matched.append(policy_record)
            decision = policy.actions.get("decision", "ALLOW")
            reason = policy.actions.get("reason") or policy.description
            if decision == "DENY":
                violations.append({"policy_id": policy.policy_id, "name": policy.name, "message": reason})
            if decision == "REQUIRE_APPROVAL":
                approval_reasons.append(reason)

        if violations:
            return {
                "decision": "DENY",
                "matching_policies": matched,
                "violated_policies": violations,
                "missing_permissions": [],
                "reasons": [item["message"] for item in violations],
            }
        if approval_reasons:
            return {
                "decision": "REQUIRE_APPROVAL",
                "matching_policies": matched,
                "violated_policies": [],
                "missing_permissions": [],
                "reasons": approval_reasons,
            }
        return {
            "decision": "ALLOW",
            "matching_policies": matched,
            "violated_policies": [],
            "missing_permissions": [],
            "reasons": [f"{service}.{operation} is permitted for {identity.get('agent_name')}."],
            "amount": amount,
        }

    def _policy_group_applies(self, policy: Policy, identity: dict) -> bool:
        groups = identity.get("policy_groups", [])
        return policy.policy_group in groups or policy.policy_group == "default"

    def _conditions_match(self, conditions: dict, identity: dict, normalized_execution: dict) -> bool:
        service = conditions.get("service")
        operation = conditions.get("operation")
        department = conditions.get("department")
        amount_greater_than = conditions.get("amount_greater_than")
        amount_less_than = conditions.get("amount_less_than")
        if service and service != normalized_execution.get("service"):
            return False
        if operation and operation != normalized_execution.get("operation"):
            return False
        if department and department != identity.get("department"):
            return False
        amount = normalized_execution.get("amount", 0)
        if amount_greater_than is not None and amount <= float(amount_greater_than):
            return False
        if amount_less_than is not None and amount >= float(amount_less_than):
            return False
        return True
