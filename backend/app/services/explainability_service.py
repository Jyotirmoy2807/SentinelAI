class ExplainabilityService:
    def generate(self, state: dict) -> dict:
        audit = state.get("audit", {})
        lines = []
        sections = []
        identity = state.get("identity", {})
        if identity:
            lines.append(identity.get("reason", "Identity context loaded."))
            sections.append({"title": "Identity", "detail": identity})
        policy = state.get("policy", {})
        if policy:
            lines.extend(policy.get("reasons", []))
            sections.append({"title": "Policy", "detail": policy})
        firewall = state.get("firewall", {})
        if firewall:
            lines.append(firewall.get("block_reason") or "AI Firewall passed.")
            sections.append({"title": "AI Firewall", "detail": firewall})
        risk = state.get("risk", {})
        if risk:
            lines.append(risk.get("explanation", "Risk score generated."))
            sections.append({"title": "Risk", "detail": risk})
        budget = state.get("budget", {})
        if budget:
            lines.extend(budget.get("reasons", []))
            sections.append({"title": "Budget", "detail": budget})
        compliance = state.get("compliance", {})
        if compliance:
            lines.extend(compliance.get("reasons", []))
            sections.append({"title": "Compliance", "detail": compliance})
        approval = state.get("approval", {})
        if approval:
            lines.append(f"Approval status is {approval.get('status')}: {approval.get('reason', '')}")
            sections.append({"title": "Human Approval", "detail": approval})
        execution = state.get("execution", {})
        if execution:
            lines.append(f"Enterprise execution status: {execution.get('status')} via {execution.get('adapter_used')}.")
            sections.append({"title": "Execution", "detail": execution})
        return {
            "summary": audit.get("decision", "PENDING"),
            "narrative": " ".join(line for line in lines if line),
            "sections": sections,
            "decision": audit.get("decision"),
            "timeline": state.get("events", []),
        }
