from app.graph.state import GovernanceState


def route_after_identity(state: GovernanceState) -> str:
    if state.get("fatal_error"):
        return "explainability_node"
    if state.get("identity", {}).get("decision") == "DENY":
        return "audit_engine"
    return "risk_engine"


def route_after_policy(state: GovernanceState) -> str:
    if state.get("fatal_error"):
        return "explainability_node"
    if state.get("policy", {}).get("decision") == "DENY":
        return "audit_engine"
    if state.get("policy", {}).get("decision") == "REQUIRE_APPROVAL":
        return "human_approval"
    return "enterprise_execution"


def route_after_human_approval(state: GovernanceState) -> str:
    if state.get("fatal_error"):
        return "explainability_node"
    status = state.get("approval", {}).get("status")
    if status == "APPROVED":
        return "enterprise_execution"
    return "audit_engine"
