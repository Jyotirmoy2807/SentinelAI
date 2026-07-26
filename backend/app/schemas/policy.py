from datetime import datetime
from typing import Any

from pydantic import Field

from app.schemas.common import ORMModel


class PolicyBase(ORMModel):
    policy_id: str
    name: str
    description: str = ""
    priority: int = 100
    status: str = "ACTIVE"
    version: str = "1.0"
    department: str = "Enterprise"
    policy_group: str = "default"
    conditions: dict[str, Any] = Field(default_factory=dict)
    actions: dict[str, Any] = Field(default_factory=dict)


class PolicyCreate(PolicyBase):
    pass


class PolicyUpdate(ORMModel):
    name: str | None = None
    description: str | None = None
    priority: int | None = None
    status: str | None = None
    version: str | None = None
    department: str | None = None
    policy_group: str | None = None
    conditions: dict[str, Any] | None = None
    actions: dict[str, Any] | None = None


class PolicyRead(PolicyBase):
    id: int
    created_at: datetime
    updated_at: datetime
