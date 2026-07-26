class PolicyService:
    def __init__(self, opa_adapter, policy_catalog):
        self.opa_adapter = opa_adapter
        self.policy_catalog = policy_catalog

    def list_policies(self) -> list[dict]:
        return self.policy_catalog.list_policies()

    def evaluate(self, identity: dict, normalized_execution: dict, risk: dict) -> dict:
        result = self.opa_adapter.evaluate(self._build_opa_input(identity, normalized_execution, risk))
        return {
            "decision": result.decision,
            "matched_policy": result.matched_policy,
            "reasons": result.reasons,
            "opa_url": result.opa_url,
            "raw_result": result.raw_result,
        }

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
