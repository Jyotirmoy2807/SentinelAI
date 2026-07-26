class ExplainabilityService:
    def generate(self, state: dict) -> dict:
        audit = state.get("audit", {})
        audit_events = audit.get("events") or state.get("events", [])
        timeline = [self._timeline_item(event) for event in audit_events if event.get("status") != "RUNNING"]
        lines = [item["description"] for item in timeline]
        return {
            "summary": audit.get("decision", "PENDING"),
            "narrative": " ".join(lines),
            "sections": [
                {"title": "Audit Timeline", "detail": timeline},
                {"title": "NIST RMF Risk", "detail": state.get("risk", {})},
                {"title": "OPA Decision", "detail": state.get("policy", {})},
            ],
            "decision": audit.get("decision"),
            "timeline": timeline,
        }

    def _timeline_item(self, event: dict) -> dict:
        stage = event.get("stage") or event.get("node")
        decision = event.get("decision") or event.get("status")
        risk = event.get("riskScore")
        description = event.get("reason") or f"{stage} completed with {decision}."
        if stage == "risk_engine" and risk is not None:
            description = f"Risk Score = {risk}."
        if stage == "policy_engine":
            description = f"OPA Policy = {decision}."
        if stage == "enterprise_execution":
            description = "Enterprise API Executed."
        if stage == "audit_splunk":
            description = "Audit Logged."
        return {
            "timestamp": event.get("timestamp"),
            "title": stage.replace("_", " ").title() if stage else "Governance Event",
            "description": description,
            "decision": decision,
            "riskScore": risk,
            "policy": event.get("policy"),
        }
