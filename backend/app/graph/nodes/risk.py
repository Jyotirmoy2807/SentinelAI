from app.graph.nodes.base import run_governance_node
from app.graph.state import EventSink, GovernanceState
from app.services.container import ServiceContainer


def build_risk_engine_node(services: ServiceContainer, event_sink: EventSink | None = None):
    async def node(state: GovernanceState) -> dict:
        async def action(current_state: GovernanceState) -> dict:
            risk = services.risk.calculate(
                current_state.get("identity", {}),
                current_state.get("normalized_execution", {}),
            )
            return {"risk": risk}

        return await run_governance_node(state, "risk_engine", action, event_sink)

    return node
