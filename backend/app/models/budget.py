from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class BudgetProfile(Base):
    __tablename__ = "budget_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    department: Mapped[str] = mapped_column(String(80), default="Enterprise")
    daily_limit: Mapped[float] = mapped_column(Float, default=5000.0)
    monthly_limit: Mapped[float] = mapped_column(Float, default=100000.0)
    transaction_limit: Mapped[float] = mapped_column(Float, default=1000.0)
    approval_threshold: Mapped[float] = mapped_column(Float, default=500.0)
    spent_today: Mapped[float] = mapped_column(Float, default=0.0)
    spent_month: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
