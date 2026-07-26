from app.graph.nodes.base import run_governance_node, status_from_decision
from app.graph.state import EventSink, GovernanceState
from app.services.container import ServiceContainer


def build_agent_identity_node(services: ServiceContainer, event_sink: EventSink | None = None):
    async def node(state: GovernanceState) -> dict:
        async def action(current_state: GovernanceState) -> dict:
            normalized = current_state.get("normalized_execution", {})
            return {"identity": services.agents.load_passport(normalized.get("passport_id", ""))}

        return await run_governance_node(state, "agent_identity", action, event_sink, status_from_decision("identity"))

    return node
