from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from app.repositories.audit_repository import AuditRepository
from app.utils.serialization import json_safe
from app.utils.time import utc_now


class AuditSink(ABC):
    @abstractmethod
    def emit(self, event: dict[str, Any]) -> None:
        pass

    @abstractmethod
    def flush(self) -> None:
        pass


class SQLiteSplunkAuditSink(AuditSink):
    def __init__(self, repository: AuditRepository):
        self.repository = repository

    def emit(self, event: dict[str, Any]) -> None:
        self.repository.create(
            {
                "event_id": event.get("eventId"),
                "request_id": event.get("requestId", ""),
                "timestamp": self._parse_timestamp(event.get("timestamp")),
                "agent": event.get("agent", ""),
                "action": event.get("action", ""),
                "policy": event.get("policy", ""),
                "risk_score": float(event.get("riskScore") or 0),
                "decision": event.get("decision", ""),
                "approval_status": event.get("approvalStatus", ""),
                "latency_ms": float(event.get("latency") or 0),
                "reason": event.get("reason", ""),
                "enterprise_api": event.get("enterpriseAPI", ""),
                "stage": event.get("stage", ""),
                "payload": json_safe(event),
            }
        )

    def flush(self) -> None:
        self.repository.db.commit()

    def _parse_timestamp(self, value: Any) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return utc_now()
        return utc_now()
