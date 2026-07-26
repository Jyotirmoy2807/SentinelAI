from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class EnterpriseAPI(Base):
    __tablename__ = "enterprise_apis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    service_name: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    adapter: Mapped[str] = mapped_column(String(80))
    version: Mapped[str] = mapped_column(String(32), default="1.0")
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", index=True)
    permissions: Mapped[list[str]] = mapped_column(JSON, default=list)
    required_policies: Mapped[list[str]] = mapped_column(JSON, default=list)
    allowed_agents: Mapped[list[str]] = mapped_column(JSON, default=list)
    endpoint_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
