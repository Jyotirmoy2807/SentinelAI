from datetime import datetime
from typing import Any

from pydantic import Field

from app.schemas.common import ORMModel


class ComplianceRuleBase(ORMModel):
    rule_id: str
    name: str
    framework: str = "Internal"
    status: str = "ACTIVE"
    version: str = "1.0"
    affected_departments: list[str] = Field(default_factory=list)
    conditions: dict[str, Any] = Field(default_factory=dict)
    require_approval: bool = False


class ComplianceRuleCreate(ComplianceRuleBase):
    pass


class ComplianceRuleUpdate(ORMModel):
    name: str | None = None
    framework: str | None = None
    status: str | None = None
    version: str | None = None
    affected_departments: list[str] | None = None
    conditions: dict[str, Any] | None = None
    require_approval: bool | None = None


class ComplianceRuleRead(ComplianceRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime
