from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ComplianceRule(Base):
    __tablename__ = "compliance_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    rule_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    framework: Mapped[str] = mapped_column(String(80), default="Internal")
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE")
    version: Mapped[str] = mapped_column(String(32), default="1.0")
    affected_departments: Mapped[list[str]] = mapped_column(JSON, default=list)
    conditions: Mapped[dict] = mapped_column(JSON, default=dict)
    require_approval: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
