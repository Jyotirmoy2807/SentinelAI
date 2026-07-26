from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class PolicyCondition(BaseModel):
    field: str
    operator: str
    value: str | int | float | bool


class GovernancePolicyBase(ORMModel):
    policy_id: str = Field(min_length=3, max_length=100, pattern=r"^[a-zA-Z0-9_-]+$")
    name: str = Field(min_length=2, max_length=160)
    description: str = ""
    decision: str = "ALLOW"
    priority: int = Field(default=100, ge=0, le=999999)
    enabled: bool = True
    conditions: list[PolicyCondition] = Field(default_factory=list)
    reason: str = ""


class GovernancePolicyCreate(GovernancePolicyBase):
    pass


class GovernancePolicyUpdate(ORMModel):
    policy_id: str | None = Field(default=None, min_length=3, max_length=100, pattern=r"^[a-zA-Z0-9_-]+$")
    name: str | None = Field(default=None, min_length=2, max_length=160)
    description: str | None = None
    decision: str | None = None
    priority: int | None = Field(default=None, ge=0, le=999999)
    enabled: bool | None = None
    conditions: list[PolicyCondition] | None = None
    reason: str | None = None


class GovernancePolicyRead(GovernancePolicyBase):
    id: int
    created_at: datetime
    updated_at: datetime


class BudgetPolicyBase(ORMModel):
    name: str = Field(min_length=2, max_length=160)
    department: str = Field(min_length=2, max_length=100)
    daily_limit: float = Field(ge=0)
    monthly_limit: float = Field(ge=0)
    transaction_limit: float = Field(ge=0)
    approval_threshold: float = Field(ge=0)
    spent_today: float = Field(default=0, ge=0)
    spent_month: float = Field(default=0, ge=0)
    status: str = "ACTIVE"


class BudgetPolicyCreate(BudgetPolicyBase):
    pass


class BudgetPolicyUpdate(ORMModel):
    name: str | None = Field(default=None, min_length=2, max_length=160)
    department: str | None = Field(default=None, min_length=2, max_length=100)
    daily_limit: float | None = Field(default=None, ge=0)
    monthly_limit: float | None = Field(default=None, ge=0)
    transaction_limit: float | None = Field(default=None, ge=0)
    approval_threshold: float | None = Field(default=None, ge=0)
    spent_today: float | None = Field(default=None, ge=0)
    spent_month: float | None = Field(default=None, ge=0)
    status: str | None = None


class BudgetPolicyRead(BudgetPolicyBase):
    id: int
    created_at: datetime
    updated_at: datetime


class PolicyVersionRead(ORMModel):
    id: int
    version_id: str
    resource_type: str
    resource_key: str
    action: str
    snapshot: dict[str, Any]
    generated_rego: str
    created_by: str
    created_at: datetime


class PolicyDeploymentRead(ORMModel):
    id: int
    deployment_id: str
    status: str
    message: str
    checksum: str
    opa_fmt_status: str
    opa_check_status: str
    opa_reload_status: str
    created_at: datetime


class PolicyCompareRead(BaseModel):
    left: PolicyVersionRead
    right: PolicyVersionRead
    changed: bool
    summary: list[str]


class PolicyLookupRead(BaseModel):
    decisions: list[str]
    statuses: list[str]
    budget_statuses: list[str]
    departments: list[str]
    condition_fields: list[dict[str, str]]
    condition_operators: list[dict[str, str]]
