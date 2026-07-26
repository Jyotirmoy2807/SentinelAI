import json
from typing import Any


class PolicyRegoGenerator:
    CONDITION_FIELDS = {
        "identity.status": "input.identity.status",
        "identity.department": "input.identity.department",
        "identity.riskTier": "input.identity.riskTier",
        "identity.trustScore": "input.identity.trustScore",
        "normalizedExecution.service": "input.normalizedExecution.service",
        "normalizedExecution.operation": "input.normalizedExecution.operation",
        "normalizedExecution.amount": "input.normalizedExecution.amount",
        "risk.score": "input.risk.score",
        "risk.level": "input.risk.level",
        "risk.category": "input.risk.category",
    }

    OPERATORS = {
        "equals": "==",
        "not_equals": "!=",
        "greater_than": ">",
        "greater_or_equal": ">=",
        "less_than": "<",
        "less_or_equal": "<=",
    }

    def render(self, governance_policies: list[Any], budget_policies: list[Any]) -> str:
        lines = [
            "package sentinelai.governance",
            "",
            'default decision := {"decision": "ALLOW", "matched_policy": "default_allow", "reasons": ["No governance or budget policy matched."]}',
            "",
            "decision := result if {",
            "  policy := selected_policy",
            '  result := {"decision": policy.decision, "matched_policy": policy.policy_id, "reasons": [policy.reason], "priority": policy.priority}',
            "}",
            "",
            "ranked_matches[key] := policy if {",
            "  some policy in policy_matches",
            '  key := sprintf("%06d:%s", [1000000 - policy.priority, policy.policy_id])',
            "}",
            "",
            "selected_policy := ranked_matches[keys[0]] if {",
            "  count(ranked_matches) > 0",
            "  keys := sort(object.keys(ranked_matches))",
            "}",
            "",
        ]
        for policy in governance_policies:
            if policy.enabled:
                lines.extend(self._governance_policy_rule(policy))
        for index, policy in enumerate(budget_policies):
            if policy.status == "ACTIVE":
                lines.extend(self._budget_policy_rules(policy, index))
        return "\n".join(lines).strip() + "\n"

    def _governance_policy_rule(self, policy: Any) -> list[str]:
        body = self._condition_lines(policy.conditions or [])

        # Always scope to agents that have opted in via their policy_groups.
        # The agent's policy_groups list is the single source of truth for which policies apply.
        body = [f'"{policy.policy_id}" in input.identity.policyGroups', *body]

        payload = self._policy_payload(
            policy_id=policy.policy_id,
            decision=policy.decision,
            priority=policy.priority,
            reason=policy.reason or policy.description or policy.name,
        )
        return [
            "policy_matches contains policy if {",
            *[f"  {line}" for line in body],
            f"  policy := {payload}",
            "}",
            "",
        ]

    def _budget_policy_rules(self, policy: Any, index: int) -> list[str]:
        base_priority = 900000 - index * 10
        policy_key = self._policy_key(policy.name)
        department = json.dumps(policy.department)
        lines: list[str] = []
        lines.extend(
            self._budget_rule(
                policy_id=f"budget_{policy_key}_transaction_limit",
                decision="DENY",
                priority=base_priority,
                reason=f"{policy.name} transaction limit exceeded.",
                department=department,
                expression=f"amount > {float(policy.transaction_limit)}",
            )
        )
        lines.extend(
            self._budget_rule(
                policy_id=f"budget_{policy_key}_daily_limit",
                decision="DENY",
                priority=base_priority - 1,
                reason=f"{policy.name} daily limit exceeded.",
                department=department,
                expression=f"amount + {float(policy.spent_today)} > {float(policy.daily_limit)}",
            )
        )
        lines.extend(
            self._budget_rule(
                policy_id=f"budget_{policy_key}_monthly_limit",
                decision="DENY",
                priority=base_priority - 2,
                reason=f"{policy.name} monthly limit exceeded.",
                department=department,
                expression=f"amount + {float(policy.spent_month)} > {float(policy.monthly_limit)}",
            )
        )
        lines.extend(
            self._budget_rule(
                policy_id=f"budget_{policy_key}_approval_threshold",
                decision="REQUIRE_APPROVAL",
                priority=base_priority - 3,
                reason=f"{policy.name} approval threshold reached.",
                department=department,
                expression=f"amount >= {float(policy.approval_threshold)}",
            )
        )
        return lines

    def _budget_rule(self, policy_id: str, decision: str, priority: int, reason: str, department: str, expression: str) -> list[str]:
        payload = self._policy_payload(policy_id=policy_id, decision=decision, priority=priority, reason=reason)
        return [
            "policy_matches contains policy if {",
            f"  input.identity.department == {department}",
            "  amount := input.normalizedExecution.amount",
            f"  {expression}",
            f"  policy := {payload}",
            "}",
            "",
        ]

    def _condition_lines(self, conditions: list[dict]) -> list[str]:
        if not conditions:
            return ["true"]
        return [self._condition_line(condition) for condition in conditions]

    def _condition_line(self, condition: dict) -> str:
        field = condition.get("field")
        operator = condition.get("operator")
        value = condition.get("value")
        rego_field = self.CONDITION_FIELDS.get(field)
        if not rego_field:
            raise ValueError(f"Unsupported condition field: {field}")
        if operator == "contains":
            return f"{json.dumps(value)} in {rego_field}"
        rego_operator = self.OPERATORS.get(operator)
        if not rego_operator:
            raise ValueError(f"Unsupported condition operator: {operator}")
        return f"{rego_field} {rego_operator} {json.dumps(value)}"

    def _policy_payload(self, policy_id: str, decision: str, priority: int, reason: str) -> str:
        return json.dumps(
            {
                "policy_id": policy_id,
                "decision": decision,
                "priority": int(priority),
                "reason": reason,
            },
            sort_keys=True,
        )

    def _policy_key(self, value: str) -> str:
        return "".join(character.lower() if character.isalnum() else "_" for character in value).strip("_")
