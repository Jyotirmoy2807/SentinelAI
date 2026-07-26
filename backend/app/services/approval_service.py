from datetime import timedelta
from uuid import uuid4

from app.models.approval import Approval
from app.repositories.approval_repository import ApprovalRepository
from app.utils.serialization import json_safe
from app.utils.time import utc_iso_ms, utc_now


class ApprovalService:
    def __init__(self, repository: ApprovalRepository):
        self.repository = repository

    def list_approvals(self) -> list[Approval]:
        return self.repository.list_recent()

    def list_pending(self) -> list[Approval]:
        return self.repository.list_pending()

    def get_approval(self, approval_id: str) -> Approval | None:
        return self.repository.get_by_approval_id(approval_id)

    def create_or_get_pending(self, state: dict) -> dict:
        metadata = state.get("metadata", {})
        normalized = state.get("normalized_execution", {})
        identity = state.get("identity", {})
        request_id = metadata.get("request_id")
        existing = self.repository.get_by_request_id(request_id)
        if existing and existing.status == "PENDING":
            return self._to_state(existing)

        approval_id = f"APR-{uuid4().hex[:10].upper()}"
        reason = self._approval_reason(state)
        approval_state = {
            "approval_id": approval_id,
            "required": True,
            "status": "PENDING",
            "approver": "Governance Manager",
            "timestamp": utc_iso_ms(),
            "comments": "",
            "reason": reason,
        }
        snapshot = {**state, "approval": approval_state}
        approval = self.repository.create(
            {
                "approval_id": approval_id,
                "request_id": request_id,
                "passport_id": identity.get("passport_id", normalized.get("passport_id", "")),
                "agent_name": identity.get("agent_name", ""),
                "service": normalized.get("service", ""),
                "operation": normalized.get("operation", ""),
                "amount": float(normalized.get("amount") or 0),
                "risk_score": float(state.get("risk", {}).get("score") or 0),
                "approver": "Governance Manager",
                "status": "PENDING",
                "reason": reason,
                "comments": "",
                "state_snapshot": json_safe(snapshot),
                "expires_at": utc_now() + timedelta(hours=8),
            }
        )
        self.repository.db.commit()
        return self._to_state(approval)

    def approve(self, approval: Approval, approver: str, comments: str) -> Approval:
        updated = self.repository.update(
            approval,
            {
                "status": "APPROVED",
                "approver": approver,
                "comments": comments,
                "updated_at": utc_now(),
            },
        )
        self.repository.db.commit()
        return updated

    def reject(self, approval: Approval, approver: str, comments: str) -> Approval:
        updated = self.repository.update(
            approval,
            {
                "status": "REJECTED",
                "approver": approver,
                "comments": comments,
                "updated_at": utc_now(),
            },
        )
        self.repository.db.commit()
        return updated

    def apply_existing_decision(self, state: dict, approval: Approval) -> dict:
        approval_state = self._to_state(approval)
        approval_state["timestamp"] = utc_iso_ms()
        return approval_state

    def _approval_reason(self, state: dict) -> str:
        reasons = []
        for section in ("policy", "risk"):
            reasons.extend(state.get(section, {}).get("reasons", []))
            if state.get(section, {}).get("explanation"):
                reasons.append(state[section]["explanation"])
        risk = state.get("risk", {})
        if risk.get("category") == "HIGH":
            reasons.append("High risk score requires human approval.")
        return " ".join(reasons) or "Human governance review required."

    def _to_state(self, approval: Approval) -> dict:
        return {
            "approval_id": approval.approval_id,
            "required": True,
            "status": approval.status,
            "approver": approval.approver,
            "timestamp": utc_iso_ms(approval.updated_at) if approval.updated_at else None,
            "comments": approval.comments,
            "reason": approval.reason,
        }
