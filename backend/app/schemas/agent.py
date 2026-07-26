from datetime import datetime

from pydantic import Field

from app.schemas.common import ORMModel


class AgentBase(ORMModel):
    passport_id: str
    name: str
    owner: str
    department: str
    version: str = "1.0.0"
    status: str = "ACTIVE"
    trust_score: float = 80.0
    risk_tier: str = "LOW"
    allowed_apis: list[str] = Field(default_factory=list)
    allowed_operations: list[str] = Field(default_factory=list)
    budget_profile: str = "Standard"
    policy_groups: list[str] = Field(default_factory=list)
    reputation: float = 90.0


class AgentCreate(AgentBase):
    pass


class AgentUpdate(ORMModel):
    name: str | None = None
    owner: str | None = None
    department: str | None = None
    version: str | None = None
    status: str | None = None
    trust_score: float | None = None
    risk_tier: str | None = None
    allowed_apis: list[str] | None = None
    allowed_operations: list[str] | None = None
    budget_profile: str | None = None
    policy_groups: list[str] | None = None
    reputation: float | None = None


class AgentRead(AgentBase):
    id: int
    last_activity: datetime | None = None
    created_at: datetime
    updated_at: datetime


class AgentPassport(ORMModel):
    passport_id: str
    agent_name: str
    owner: str
    department: str
    version: str
    status: str
    trust_score: float
    reputation: float
    risk_tier: str
    allowed_apis: list[str]
    allowed_operations: list[str]
    policy_groups: list[str]
    budget_profile: str
