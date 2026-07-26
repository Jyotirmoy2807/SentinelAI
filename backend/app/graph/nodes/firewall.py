from app.graph.nodes.base import run_governance_node, status_from_decision
from app.graph.state import EventSink, GovernanceState
from app.services.container import ServiceContainer


def build_ai_firewall_node(services: ServiceContainer, event_sink: EventSink | None = None):
    async def node(state: GovernanceState) -> dict:
        async def action(current_state: GovernanceState) -> dict:
            firewall = services.firewall.inspect(current_state.get("normalized_execution", {}))
            return {"firewall": firewall}

        return await run_governance_node(state, "ai_firewall", action, event_sink, status_from_decision("firewall"))

    return node
