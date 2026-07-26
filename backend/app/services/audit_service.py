from datetime import datetime
from uuid import uuid4

from app.adapters.audit_sink import AuditSink
from app.repositories.audit_repository import AuditRepository
from app.repositories.governance_request_repository import GovernanceRequestRepository
from app.utils.serialization import json_safe


class AuditService:
    def __init__(
        self,
        audit_repository: AuditRepository,
        request_repository: GovernanceRequestRepository,
        sink: AuditSink,
    ):
        self.audit_repository = audit_repository
        self.request_repository = request_repository
        self.sink = sink

    def record(self, state: dict) -> dict:
        metadata = state.get("metadata", {})
        normalized = state.get("normalized_execution", {})
        request_id = metadata.get("request_id", "")
        decision = self.resolve_decision(state)
        status = self._status_from_decision(decision, state)
        risk_score = float(state.get("risk", {}).get("score") or 0)
        existing_request = self.request_repository.get_by_request_id(request_id)
        request_data = {
            "request_id": request_id,
            "trace_id": metadata.get("trace_id", ""),
            "passport_id": normalized.get("passport_id", state.get("identity", {}).get("passport_id", "")),
            "service": normalized.get("service", ""),
            "operation": normalized.get("operation", ""),
            "status": status,
            "decision": decision,
            "risk_score": risk_score,
            "duration_ms": float(metadata.get("execution_duration_ms") or 0),
            "state_snapshot": json_safe(state),
            "completed_at": None if decision == "REQUIRE_APPROVAL" else datetime.utcnow(),
        }
        if existing_request:
            self.request_repository.update(existing_request, request_data)
        else:
            self.request_repository.create(request_data)

        events = self._splunk_events(state, decision)
        for event in events:
            self.sink.emit(event)
        self.sink.flush()
        return {
            "audit_id": f"AUD-{uuid4().hex[:10].upper()}",
            "decision": decision,
            "status": status,
            "events": events,
            "event_timeline": events,
            "decision_trail": self._decision_trail(state),
            "node_history": [event.get("stage") for event in events],
        }

    def list_recent(self, limit: int = 200) -> list:
        return self.audit_repository.list_recent(limit)

    def detail(self, request_id: str, execution_logs: list) -> dict:
        return {
            "request_id": request_id,
            "audit_logs": self.audit_repository.list_by_request(request_id),
            "execution_logs": execution_logs,
        }

    def resolve_decision(self, state: dict) -> str:
        if state.get("identity", {}).get("decision") == "DENY":
            return "DENY"
        approval_status = state.get("approval", {}).get("status")
        if approval_status == "PENDING":
            return "REQUIRE_APPROVAL"
        if approval_status == "REJECTED":
            return "DENY"
        if state.get("policy", {}).get("decision") == "DENY":
            return "DENY"
        if state.get("policy", {}).get("decision") == "REQUIRE_APPROVAL" and approval_status != "APPROVED":
            return "REQUIRE_APPROVAL"
        return "ALLOW"

    def _status_from_decision(self, decision: str, state: dict) -> str:
        if decision == "REQUIRE_APPROVAL":
            return "PENDING_APPROVAL"
        if decision == "DENY":
            return "DENIED"
        if state.get("simulation"):
            return "SIMULATED"
        return "APPROVED"

    def _decision_message(self, decision: str, state: dict) -> str:
        if decision == "ALLOW":
            return "Governance approved the enterprise execution path."
        if decision == "REQUIRE_APPROVAL":
            return "Governance paused execution pending human approval."
        return "Governance denied the enterprise execution path."

    def _decision_trail(self, state: dict) -> list[dict]:
        trail = []
        for section in ("identity", "risk", "policy", "approval", "execution"):
            payload = state.get(section)
            if payload:
                trail.append({"section": section, "decision": payload.get("decision") or payload.get("status"), "payload": payload})
        return trail

    def _splunk_events(self, state: dict, final_decision: str) -> list[dict]:
        events = [event for event in state.get("events", []) if event.get("status") != "RUNNING"]
        audit_event = self._build_audit_logged_event(state, final_decision)
        return events + [audit_event]

    def _build_audit_logged_event(self, state: dict, final_decision: str) -> dict:
        metadata = state.get("metadata", {})
        identity = state.get("identity", {})
        normalized = state.get("normalized_execution", {})
        policy = state.get("policy", {})
        risk = state.get("risk", {})
        approval = state.get("approval", {})
        return {
            "eventId": f"EVT-{uuid4().hex[:12].upper()}",
            "timestamp": metadata.get("timestamp"),
            "requestId": metadata.get("request_id", ""),
            "request_id": metadata.get("request_id", ""),
            "agent": identity.get("agent_name") or identity.get("passport_id") or normalized.get("passport_id", ""),
            "action": normalized.get("operation", ""),
            "policy": policy.get("matched_policy", ""),
            "riskScore": risk.get("score", 0),
            "decision": final_decision,
            "approvalStatus": approval.get("status", "NOT_REQUIRED"),
            "latency": 0,
            "duration_ms": 0,
            "reason": self._decision_message(final_decision, state),
            "enterpriseAPI": normalized.get("service", ""),
            "stage": "audit_splunk",
            "node": "audit_splunk",
            "status": "COMPLETED",
            "payload": {"sink": "splunk-compatible-json"},
        }
