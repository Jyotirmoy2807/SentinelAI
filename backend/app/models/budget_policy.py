from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.utils.time import utc_now


class BudgetPolicy(Base):
    __tablename__ = "budget_policies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    department: Mapped[str] = mapped_column(String(100), index=True)
    daily_limit: Mapped[float] = mapped_column(Float, default=0.0)
    monthly_limit: Mapped[float] = mapped_column(Float, default=0.0)
    transaction_limit: Mapped[float] = mapped_column(Float, default=0.0)
    approval_threshold: Mapped[float] = mapped_column(Float, default=0.0)
    spent_today: Mapped[float] = mapped_column(Float, default=0.0)
    spent_month: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
