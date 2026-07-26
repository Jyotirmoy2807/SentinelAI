class ResponseBuilderService:
    def build(self, state: dict) -> dict:
        audit = state.get("audit", {})
        approval = state.get("approval", {})
        risk = state.get("risk", {})
        decision = audit.get("decision", "ERROR")
        return {
            "metadata": {
                **state.get("metadata", {}),
                "request_id": state.get("metadata", {}).get("request_id"),
                "trace_id": state.get("metadata", {}).get("trace_id"),
            },
            "governance": {
                "decision": decision,
                "risk": risk,
                "reasons": self._collect_reasons(state),
                "approval_status": approval.get("status", "NOT_REQUIRED"),
                "status": audit.get("status"),
            },
            "result": state.get("execution"),
            "explainability": state.get("explainability", {}),
            "state": self._public_state(state),
        }

    def _collect_reasons(self, state: dict) -> list[str]:
        reasons = []
        for section in ("identity", "policy", "firewall", "risk", "budget", "compliance", "approval"):
            payload = state.get(section, {})
            if payload.get("reason"):
                reasons.append(payload["reason"])
            reasons.extend(payload.get("reasons", []))
            if payload.get("block_reason"):
                reasons.append(payload["block_reason"])
        return [reason for reason in reasons if reason]

    def _public_state(self, state: dict) -> dict:
        return {
            key: value
            for key, value in state.items()
            if key
            in {
                "request",
                "metadata",
                "identity",
                "normalized_execution",
                "policy",
                "firewall",
                "risk",
                "budget",
                "compliance",
                "approval",
                "audit",
                "execution",
                "explainability",
                "events",
                "simulation",
            }
        }
