from app.graph.nodes.base import run_governance_node, status_from_decision
from app.graph.state import EventSink, GovernanceState
from app.services.container import ServiceContainer


def build_human_approval_node(services: ServiceContainer, event_sink: EventSink | None = None):
    async def node(state: GovernanceState) -> dict:
        async def action(current_state: GovernanceState) -> dict:
            existing = current_state.get("approval", {})
            if existing.get("status") in {"APPROVED", "REJECTED"}:
                return {"approval": existing}
            return {"approval": services.approvals.create_or_get_pending(current_state)}

        return await run_governance_node(state, "human_approval", action, event_sink, status_from_decision("approval"))

    return node
