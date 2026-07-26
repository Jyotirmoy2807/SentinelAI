from datetime import datetime
from uuid import uuid4

from app.repositories.audit_repository import AuditRepository
from app.repositories.governance_decision_repository import GovernanceDecisionRepository
from app.repositories.governance_request_repository import GovernanceRequestRepository
from app.utils.serialization import json_safe


class AuditService:
    def __init__(
        self,
        audit_repository: AuditRepository,
        request_repository: GovernanceRequestRepository,
        decision_repository: GovernanceDecisionRepository,
    ):
        self.audit_repository = audit_repository
        self.request_repository = request_repository
        self.decision_repository = decision_repository

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
            "completed_at": datetime.utcnow() if decision != "REQUIRE_APPROVAL" else None,
        }
        if existing_request:
            self.request_repository.update(existing_request, request_data)
        else:
            self.request_repository.create(request_data)

        audit_id = f"AUD-{uuid4().hex[:10].upper()}"
        self.audit_repository.create(
            {
                "audit_id": audit_id,
                "request_id": request_id,
                "event_type": "GOVERNANCE_DECISION",
                "node": "audit_engine",
                "decision": decision,
                "message": self._decision_message(decision, state),
                "payload": json_safe(
                    {
                        "identity": state.get("identity"),
                        "policy": state.get("policy"),
                        "firewall": state.get("firewall"),
                        "risk": state.get("risk"),
                        "budget": state.get("budget"),
                        "compliance": state.get("compliance"),
                        "approval": state.get("approval"),
                    }
                ),
            }
        )
        self.decision_repository.create(
            {
                "request_id": request_id,
                "decision": decision,
                "node": "audit_engine",
                "reason": self._decision_message(decision, state),
                "payload": json_safe(state),
            }
        )
        self.audit_repository.db.commit()
        return {
            "audit_id": audit_id,
            "decision": decision,
            "status": status,
            "event_timeline": state.get("events", []),
            "decision_trail": self._decision_trail(state),
            "node_history": [event.get("node") for event in state.get("events", []) if event.get("status") != "RUNNING"],
            "timestamp": datetime.utcnow().isoformat(),
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
        for section in ("identity", "policy", "firewall", "budget"):
            if state.get(section, {}).get("decision") == "DENY":
                return "DENY"
        if state.get("compliance", {}).get("decision") == "DENY":
            return "DENY"
        approval_status = state.get("approval", {}).get("status")
        if approval_status == "PENDING":
            return "REQUIRE_APPROVAL"
        if approval_status == "REJECTED":
            return "DENY"
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
        for section in ("identity", "policy", "firewall", "risk", "budget", "compliance", "approval"):
            payload = state.get(section)
            if payload:
                trail.append({"section": section, "decision": payload.get("decision") or payload.get("status"), "payload": payload})
        return trail
