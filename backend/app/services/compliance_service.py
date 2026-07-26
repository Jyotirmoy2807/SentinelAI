from app.models.compliance_rule import ComplianceRule
from app.repositories.compliance_repository import ComplianceRepository


class ComplianceService:
    def __init__(self, repository: ComplianceRepository):
        self.repository = repository

    def list_rules(self) -> list[ComplianceRule]:
        return self.repository.list()

    def get_rule(self, rule_id: int) -> ComplianceRule | None:
        return self.repository.get(rule_id)

    def create_rule(self, data: dict) -> ComplianceRule:
        rule = self.repository.create(data)
        self.repository.db.commit()
        return rule

    def update_rule(self, rule: ComplianceRule, data: dict) -> ComplianceRule:
        updated = self.repository.update(rule, data)
        self.repository.db.commit()
        return updated

    def delete_rule(self, rule: ComplianceRule) -> ComplianceRule:
        updated = self.repository.update(rule, {"status": "DELETED"})
        self.repository.db.commit()
        return updated

    def evaluate(self, identity: dict, normalized_execution: dict, risk: dict) -> dict:
        violations = []
        regulatory_flags = []
        internal_flags = []
        approval_required = False

        for rule in self.repository.list_active():
            if not self._rule_applies(rule, identity, normalized_execution, risk):
                continue
            record = {
                "rule_id": rule.rule_id,
                "name": rule.name,
                "framework": rule.framework,
                "version": rule.version,
            }
            if rule.require_approval:
                approval_required = True
                regulatory_flags.append(record)
            elif rule.conditions.get("decision") == "FAIL":
                violations.append(record)
            else:
                internal_flags.append(record)

        if violations:
            return {
                "decision": "DENY",
                "rules": regulatory_flags + internal_flags,
                "violations": violations,
                "regulatory_flags": regulatory_flags,
                "internal_policy_flags": internal_flags,
                "approval_required": False,
                "reasons": [f"{item['name']} produced a compliance violation." for item in violations],
            }
        if approval_required:
            return {
                "decision": "REQUIRE_APPROVAL",
                "rules": regulatory_flags + internal_flags,
                "violations": [],
                "regulatory_flags": regulatory_flags,
                "internal_policy_flags": internal_flags,
                "approval_required": True,
                "reasons": [f"{item['name']} requires human review." for item in regulatory_flags],
            }
        return {
            "decision": "PASS",
            "rules": internal_flags,
            "violations": [],
            "regulatory_flags": regulatory_flags,
            "internal_policy_flags": internal_flags,
            "approval_required": False,
            "reasons": ["Compliance checks passed."],
        }

    def _rule_applies(self, rule: ComplianceRule, identity: dict, normalized_execution: dict, risk: dict) -> bool:
        departments = rule.affected_departments or []
        if departments and identity.get("department") not in departments and "All" not in departments:
            return False
        conditions = rule.conditions or {}
        service = conditions.get("service")
        operation = conditions.get("operation")
        amount_greater_than = conditions.get("amount_greater_than")
        risk_greater_than = conditions.get("risk_greater_than")
        if service and service != normalized_execution.get("service"):
            return False
        if operation and operation != normalized_execution.get("operation"):
            return False
        if amount_greater_than is not None and float(normalized_execution.get("amount") or 0) <= float(amount_greater_than):
            return False
        if risk_greater_than is not None and float(risk.get("score") or 0) <= float(risk_greater_than):
            return False
        return True
