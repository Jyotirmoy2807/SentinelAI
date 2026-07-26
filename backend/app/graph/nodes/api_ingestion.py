from app.graph.nodes.base import run_governance_node
from app.graph.state import EventSink, GovernanceState
from app.services.container import ServiceContainer


def build_api_ingestion_node(services: ServiceContainer, event_sink: EventSink | None = None):
    async def node(state: GovernanceState) -> dict:
        async def action(current_state: GovernanceState) -> dict:
            raw_request = current_state.get("incoming_request", {})
            simulation = bool(current_state.get("simulation", False))
            return services.ingestion.initialize_state(raw_request, simulation)

        return await run_governance_node(state, "api_ingestion", action, event_sink)

    return node
