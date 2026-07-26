from app.graph.nodes.base import run_governance_node, status_from_decision
from app.graph.state import EventSink, GovernanceState
from app.services.container import ServiceContainer


def build_enterprise_execution_node(services: ServiceContainer, event_sink: EventSink | None = None):
    async def node(state: GovernanceState) -> dict:
        async def action(current_state: GovernanceState) -> dict:
            request_id = current_state.get("metadata", {}).get("request_id", "")
            if current_state.get("simulation"):
                return {"execution": services.execution.simulate(request_id, current_state.get("normalized_execution", {}))}
            return {"execution": services.execution.execute(request_id, current_state.get("normalized_execution", {}))}

        return await run_governance_node(state, "enterprise_execution", action, event_sink, status_from_decision("execution"))

    return node
