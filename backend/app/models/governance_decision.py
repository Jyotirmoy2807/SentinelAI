from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class GovernanceDecision(Base):
    __tablename__ = "governance_decisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    request_id: Mapped[str] = mapped_column(String(80), index=True)
    decision: Mapped[str] = mapped_column(String(32), index=True)
    node: Mapped[str] = mapped_column(String(80), default="")
    reason: Mapped[str] = mapped_column(String(1000), default="")
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
