from app.graph.nodes.base import run_governance_node
from app.graph.state import EventSink, GovernanceState
from app.services.container import ServiceContainer


def build_audit_engine_node(services: ServiceContainer, event_sink: EventSink | None = None):
    async def node(state: GovernanceState) -> dict:
        async def action(current_state: GovernanceState) -> dict:
            return {"audit": services.audit.record(current_state)}

        return await run_governance_node(state, "audit_engine", action, event_sink)

    return node
