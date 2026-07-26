from app.graph.nodes.base import run_governance_node
from app.graph.state import EventSink, GovernanceState
from app.services.container import ServiceContainer


def build_explainability_node(services: ServiceContainer, event_sink: EventSink | None = None):
    async def node(state: GovernanceState) -> dict:
        async def action(current_state: GovernanceState) -> dict:
            return {"explainability": services.explainability.generate(current_state)}

        return await run_governance_node(state, "explainability", action, event_sink)

    return node
