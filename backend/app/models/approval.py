from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.utils.time import utc_now


class Approval(Base):
    __tablename__ = "approvals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    approval_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    request_id: Mapped[str] = mapped_column(String(80), index=True)
    passport_id: Mapped[str] = mapped_column(String(64), index=True)
    agent_name: Mapped[str] = mapped_column(String(160), default="")
    service: Mapped[str] = mapped_column(String(160), default="")
    operation: Mapped[str] = mapped_column(String(160), default="")
    amount: Mapped[float] = mapped_column(Float, default=0.0)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    approver: Mapped[str] = mapped_column(String(160), default="Governance Manager")
    status: Mapped[str] = mapped_column(String(32), default="PENDING", index=True)
    reason: Mapped[str] = mapped_column(String(500), default="")
    comments: Mapped[str] = mapped_column(String(1000), default="")
    state_snapshot: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
