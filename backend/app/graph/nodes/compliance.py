from app.graph.nodes.base import run_governance_node, status_from_decision
from app.graph.state import EventSink, GovernanceState
from app.services.container import ServiceContainer


def build_compliance_engine_node(services: ServiceContainer, event_sink: EventSink | None = None):
    async def node(state: GovernanceState) -> dict:
        async def action(current_state: GovernanceState) -> dict:
            compliance = services.compliance.evaluate(
                current_state.get("identity", {}),
                current_state.get("normalized_execution", {}),
                current_state.get("risk", {}),
            )
            return {"compliance": compliance}

        return await run_governance_node(state, "compliance_engine", action, event_sink, status_from_decision("compliance"))

    return node
