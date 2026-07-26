class ResponseBuilderService:
    def build(self, state: dict) -> dict:
        audit = state.get("audit", {})
        risk = state.get("risk", {})
        decision = audit.get("decision", "ERROR")
        response = {
            "governance": {
                "requestId": state.get("metadata", {}).get("request_id", ""),
                "decision": decision,
                "riskScore": risk.get("score", 0),
                "auditId": audit.get("audit_id", ""),
            },
            "result": self._result(state, decision),
        }
        reasons = self._collect_reasons(state)
        if decision != "ALLOW" and reasons:
            response["governance"]["reason"] = reasons[0]
        return response

    def _collect_reasons(self, state: dict) -> list[str]:
        reasons = []
        for section in ("identity", "risk", "policy", "approval", "execution"):
            payload = state.get(section, {})
            if payload.get("reason"):
                reasons.append(payload["reason"])
            reasons.extend(payload.get("reasons", []))
            if payload.get("block_reason"):
                reasons.append(payload["block_reason"])
        return [reason for reason in reasons if reason]

    def _result(self, state: dict, decision: str) -> dict | None:
        if decision != "ALLOW":
            return None
        execution = state.get("execution") or {}
        return execution.get("enterprise_response") or execution
