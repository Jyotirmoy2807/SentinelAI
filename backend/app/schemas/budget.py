from datetime import datetime

from app.schemas.common import ORMModel


class BudgetProfileBase(ORMModel):
    name: str
    department: str = "Enterprise"
    daily_limit: float = 5000.0
    monthly_limit: float = 100000.0
    transaction_limit: float = 1000.0
    approval_threshold: float = 500.0
    spent_today: float = 0.0
    spent_month: float = 0.0
    status: str = "ACTIVE"


class BudgetProfileCreate(BudgetProfileBase):
    pass


class BudgetProfileUpdate(ORMModel):
    department: str | None = None
    daily_limit: float | None = None
    monthly_limit: float | None = None
    transaction_limit: float | None = None
    approval_threshold: float | None = None
    spent_today: float | None = None
    spent_month: float | None = None
    status: str | None = None


class BudgetProfileRead(BudgetProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime
