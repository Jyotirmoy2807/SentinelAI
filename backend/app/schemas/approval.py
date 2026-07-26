from datetime import datetime
from typing import Any

from pydantic import Field

from app.schemas.common import ORMModel


class ApprovalRead(ORMModel):
    id: int
    approval_id: str
    request_id: str
    passport_id: str
    agent_name: str
    service: str
    operation: str
    amount: float
    risk_score: float
    approver: str
    status: str
    reason: str
    comments: str
    state_snapshot: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
    expires_at: datetime | None = None


class ApprovalAction(ORMModel):
    approver: str = "Governance Manager"
    comments: str = ""
