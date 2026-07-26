from app.models.firewall_rule import FirewallRule
from app.repositories.firewall_repository import FirewallRepository


class FirewallService:
    def __init__(self, repository: FirewallRepository):
        self.repository = repository

    def list_rules(self) -> list[FirewallRule]:
        return self.repository.list()

    def get_rule(self, rule_id: int) -> FirewallRule | None:
        return self.repository.get(rule_id)

    def create_rule(self, data: dict) -> FirewallRule:
        rule = self.repository.create(data)
        self.repository.db.commit()
        return rule

    def update_rule(self, rule: FirewallRule, data: dict) -> FirewallRule:
        updated = self.repository.update(rule, data)
        self.repository.db.commit()
        return updated

    def delete_rule(self, rule: FirewallRule) -> FirewallRule:
        updated = self.repository.update(rule, {"status": "DELETED"})
        self.repository.db.commit()
        return updated

    def inspect(self, normalized_execution: dict) -> dict:
        service = normalized_execution.get("service")
        operation = normalized_execution.get("operation")
        parameter_text = str(normalized_execution.get("parameters", {})).lower()
        matched_rules = []
        for rule in self.repository.list_active():
            if self._matches_rule(rule, service, operation, parameter_text):
                matched_rules.append(
                    {
                        "rule_id": rule.rule_id,
                        "name": rule.name,
                        "category": rule.category,
                        "severity": rule.severity,
                        "reason": f"Matched firewall rule {rule.name}.",
                    }
                )
        if matched_rules:
            return {
                "decision": "DENY",
                "forbidden_operations": [operation],
                "dangerous_prompts": [rule["name"] for rule in matched_rules],
                "restricted_apis": [service],
                "block_reason": matched_rules[0]["reason"],
                "matched_rules": matched_rules,
            }
        return {
            "decision": "ALLOW",
            "forbidden_operations": [],
            "dangerous_prompts": [],
            "restricted_apis": [],
            "block_reason": "",
            "matched_rules": [],
        }

    def _matches_rule(self, rule: FirewallRule, service: str, operation: str, parameter_text: str) -> bool:
        if service in (rule.blocked_services or []):
            return True
        if operation in (rule.blocked_operations or []):
            return True
        return bool(rule.pattern and rule.pattern.lower() in parameter_text)
