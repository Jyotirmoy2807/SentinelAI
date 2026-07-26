from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class GovernanceDecision(str, Enum):
    allow = "ALLOW"
    deny = "DENY"
    require_approval = "REQUIRE_APPROVAL"
    escalate = "ESCALATE"
    error = "ERROR"


class EntityStatus(str, Enum):
    active = "ACTIVE"
    inactive = "INACTIVE"
    suspended = "SUSPENDED"
    blocked = "BLOCKED"
    maintenance = "MAINTENANCE"
    deleted = "DELETED"


class APIMessage(BaseModel):
    message: str


class JSONEnvelope(BaseModel):
    data: dict[str, Any] = Field(default_factory=dict)


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
