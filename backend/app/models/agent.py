from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.utils.time import utc_now


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    passport_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160), index=True)
    owner: Mapped[str] = mapped_column(String(160))
    department: Mapped[str] = mapped_column(String(80), index=True)
    version: Mapped[str] = mapped_column(String(32), default="1.0.0")
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", index=True)
    trust_score: Mapped[float] = mapped_column(Float, default=80.0)
    risk_tier: Mapped[str] = mapped_column(String(32), default="LOW")
    allowed_apis: Mapped[list[str]] = mapped_column(JSON, default=list)
    allowed_operations: Mapped[list[str]] = mapped_column(JSON, default=list)
    budget_profile: Mapped[str] = mapped_column(String(80), default="Standard")
    policy_groups: Mapped[list[str]] = mapped_column(JSON, default=list)
    reputation: Mapped[float] = mapped_column(Float, default=90.0)
    last_activity: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )
