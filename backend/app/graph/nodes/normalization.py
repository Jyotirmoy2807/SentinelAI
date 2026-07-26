from app.graph.nodes.base import run_governance_node
from app.graph.state import EventSink, GovernanceState
from app.services.container import ServiceContainer


def build_request_normalization_node(services: ServiceContainer, event_sink: EventSink | None = None):
    async def node(state: GovernanceState) -> dict:
        async def action(current_state: GovernanceState) -> dict:
            return {"normalized_execution": services.normalization.normalize(current_state.get("request", {}).get("raw", {}))}

        return await run_governance_node(state, "request_normalization", action, event_sink)

    return node
