from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class FirewallRule(Base):
    __tablename__ = "firewall_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    rule_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    category: Mapped[str] = mapped_column(String(80), default="Safety")
    severity: Mapped[str] = mapped_column(String(32), default="MEDIUM")
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE")
    pattern: Mapped[str] = mapped_column(String(240), default="")
    blocked_services: Mapped[list[str]] = mapped_column(JSON, default=list)
    blocked_operations: Mapped[list[str]] = mapped_column(JSON, default=list)
    updated_by: Mapped[str] = mapped_column(String(120), default="system")
    version: Mapped[str] = mapped_column(String(32), default="1.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
