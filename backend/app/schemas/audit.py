from datetime import datetime
from typing import Any

from pydantic import Field

from app.schemas.common import ORMModel


class AuditLogRead(ORMModel):
    id: int
    event_id: str
    request_id: str
    timestamp: datetime
    agent: str
    action: str
    policy: str
    risk_score: float
    decision: str
    approval_status: str
    latency_ms: float
    reason: str
    enterprise_api: str
    stage: str
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class ExecutionLogRead(ORMModel):
    id: int
    execution_id: str
    request_id: str
    executor: str
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
