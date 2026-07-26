from langgraph.graph import END, StateGraph

from app.graph.nodes.api_ingestion import build_api_ingestion_node
from app.graph.nodes.approval import build_human_approval_node
from app.graph.nodes.audit import build_audit_engine_node
from app.graph.nodes.execution import build_enterprise_execution_node
from app.graph.nodes.explainability import build_explainability_node
from app.graph.nodes.identity import build_agent_identity_node
from app.graph.nodes.normalization import build_request_normalization_node
from app.graph.nodes.policy import build_policy_engine_node
from app.graph.nodes.response_builder import build_response_builder_node
from app.graph.nodes.risk import build_risk_engine_node
from app.graph.routing import (
    route_after_identity,
    route_after_policy,
    route_after_human_approval,
)
from app.graph.state import EventSink, GovernanceState
from app.services.container import ServiceContainer
from app.utils.serialization import json_safe


class GovernanceGraph:
    def __init__(self, services: ServiceContainer, event_sink: EventSink | None = None):
        self.services = services
        self.event_sink = event_sink
        self.graph = self._build_full_graph()
        self.resume_graph = self._build_resume_graph()

    async def execute(self, request: dict, simulation: bool = False) -> dict:
        state: GovernanceState = {"incoming_request": request, "simulation": simulation, "events": []}
        result = await self.graph.ainvoke(state)
        return json_safe(result)

    async def resume(self, state_snapshot: dict, approval_status: str, approver: str, comments: str) -> dict:
        approval = state_snapshot.get("approval", {})
        approval.update({"status": approval_status, "approver": approver, "comments": comments})
        state_snapshot["approval"] = approval
        result = await self.resume_graph.ainvoke(state_snapshot)
        return json_safe(result)

    def _build_full_graph(self):
        workflow = StateGraph(GovernanceState)
        self._add_nodes(workflow)
        workflow.set_entry_point("api_ingestion")
        workflow.add_edge("api_ingestion", "request_normalization")
        workflow.add_edge("request_normalization", "agent_identity")
        workflow.add_conditional_edges("agent_identity", route_after_identity)
        workflow.add_edge("risk_engine", "policy_engine")
        workflow.add_conditional_edges("policy_engine", route_after_policy)
        workflow.add_conditional_edges("human_approval", route_after_human_approval)
        workflow.add_edge("enterprise_execution", "audit_engine")
        workflow.add_edge("audit_engine", "explainability_node")
        workflow.add_edge("explainability_node", "response_builder")
        workflow.add_edge("response_builder", END)
        return workflow.compile()

    def _build_resume_graph(self):
        workflow = StateGraph(GovernanceState)
        workflow.add_node("human_approval", build_human_approval_node(self.services, self.event_sink))
        workflow.add_node("audit_engine", build_audit_engine_node(self.services, self.event_sink))
        workflow.add_node("enterprise_execution", build_enterprise_execution_node(self.services, self.event_sink))
        workflow.add_node("explainability_node", build_explainability_node(self.services, self.event_sink))
        workflow.add_node("response_builder", build_response_builder_node(self.services, self.event_sink))
        workflow.set_entry_point("human_approval")
        workflow.add_conditional_edges("human_approval", route_after_human_approval)
        workflow.add_edge("enterprise_execution", "audit_engine")
        workflow.add_edge("audit_engine", "explainability_node")
        workflow.add_edge("explainability_node", "response_builder")
        workflow.add_edge("response_builder", END)
        return workflow.compile()

    def _add_nodes(self, workflow: StateGraph) -> None:
        workflow.add_node("api_ingestion", build_api_ingestion_node(self.services, self.event_sink))
        workflow.add_node("request_normalization", build_request_normalization_node(self.services, self.event_sink))
        workflow.add_node("agent_identity", build_agent_identity_node(self.services, self.event_sink))
        workflow.add_node("risk_engine", build_risk_engine_node(self.services, self.event_sink))
        workflow.add_node("policy_engine", build_policy_engine_node(self.services, self.event_sink))
        workflow.add_node("human_approval", build_human_approval_node(self.services, self.event_sink))
        workflow.add_node("audit_engine", build_audit_engine_node(self.services, self.event_sink))
        workflow.add_node("enterprise_execution", build_enterprise_execution_node(self.services, self.event_sink))
        workflow.add_node("explainability_node", build_explainability_node(self.services, self.event_sink))
        workflow.add_node("response_builder", build_response_builder_node(self.services, self.event_sink))
