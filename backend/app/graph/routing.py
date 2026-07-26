from app.graph.state import GovernanceState


def route_after_identity(state: GovernanceState) -> str:
    if state.get("fatal_error"):
        return "explainability_node"
    if state.get("identity", {}).get("decision") == "DENY":
        return "audit_engine"
    return "policy_engine"


def route_after_policy(state: GovernanceState) -> str:
    if state.get("fatal_error"):
        return "explainability_node"
    if state.get("policy", {}).get("decision") == "DENY":
        return "audit_engine"
    return "ai_firewall"


def route_after_firewall(state: GovernanceState) -> str:
    if state.get("fatal_error"):
        return "explainability_node"
    if state.get("firewall", {}).get("decision") == "DENY":
        return "audit_engine"
    return "risk_engine"


def route_after_risk(state: GovernanceState) -> str:
    if state.get("fatal_error"):
        return "explainability_node"
    return "budget_engine"


def route_after_budget(state: GovernanceState) -> str:
    if state.get("fatal_error"):
        return "explainability_node"
    if state.get("budget", {}).get("decision") == "DENY":
        return "audit_engine"
    return "compliance_engine"


def route_after_compliance(state: GovernanceState) -> str:
    if state.get("fatal_error"):
        return "explainability_node"
    if state.get("compliance", {}).get("decision") == "DENY":
        return "audit_engine"
    if _approval_needed(state):
        return "human_approval"
    return "audit_engine"


def route_after_audit(state: GovernanceState) -> str:
    if state.get("audit", {}).get("decision") == "ALLOW":
        return "enterprise_execution"
    return "explainability_node"


def _approval_needed(state: GovernanceState) -> bool:
    if state.get("policy", {}).get("decision") == "REQUIRE_APPROVAL":
        return True
    if state.get("budget", {}).get("decision") == "REQUIRE_APPROVAL":
        return True
    if state.get("compliance", {}).get("approval_required"):
        return True
    if float(state.get("risk", {}).get("score") or 0) >= 70:
        return True
    return False
