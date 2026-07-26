from datetime import datetime

from pydantic import Field

from app.schemas.common import ORMModel


class FirewallRuleBase(ORMModel):
    rule_id: str
    name: str
    category: str = "Safety"
    severity: str = "MEDIUM"
    status: str = "ACTIVE"
    pattern: str = ""
    blocked_services: list[str] = Field(default_factory=list)
    blocked_operations: list[str] = Field(default_factory=list)
    updated_by: str = "system"
    version: str = "1.0"


class FirewallRuleCreate(FirewallRuleBase):
    pass


class FirewallRuleUpdate(ORMModel):
    name: str | None = None
    category: str | None = None
    severity: str | None = None
    status: str | None = None
    pattern: str | None = None
    blocked_services: list[str] | None = None
    blocked_operations: list[str] | None = None
    updated_by: str | None = None
    version: str | None = None


class FirewallRuleRead(FirewallRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime
