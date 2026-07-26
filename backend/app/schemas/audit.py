from datetime import datetime
from typing import Any

from pydantic import Field

from app.schemas.common import ORMModel


class AuditLogRead(ORMModel):
    id: int
    audit_id: str
    request_id: str
    event_type: str
    node: str
    decision: str
    message: str
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class ExecutionLogRead(ORMModel):
    id: int
    execution_id: str
    request_id: str
    adapter: str
    enterprise_status: str
    response_code: str
    latency_ms: float
    retries: int
    request_payload: dict[str, Any]
    response_payload: dict[str, Any]
    executed_at: datetime


class AuditDetail(ORMModel):
    request_id: str
    audit_logs: list[AuditLogRead]
    execution_logs: list[ExecutionLogRead]
