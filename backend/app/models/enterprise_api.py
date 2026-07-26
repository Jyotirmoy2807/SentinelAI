from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.utils.time import utc_now


class EnterpriseAPI(Base):
    __tablename__ = "enterprise_apis"
    __table_args__ = (UniqueConstraint("service_name", "operation", name="uq_enterprise_api_operation"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    service_name: Mapped[str] = mapped_column(String(160), index=True)
    operation: Mapped[str] = mapped_column(String(120), index=True)
    method: Mapped[str] = mapped_column(String(16), default="POST")
    base_url: Mapped[str] = mapped_column(String(512))
    path: Mapped[str] = mapped_column(String(512))
    authentication_type: Mapped[str] = mapped_column(String(64), default="NONE")
    authentication_config: Mapped[dict] = mapped_column(JSON, default=dict)
    timeout_seconds: Mapped[int] = mapped_column(Integer, default=30)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    version: Mapped[str] = mapped_column(String(32), default="1.0")
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", index=True)
    required_policies: Mapped[list[str]] = mapped_column(JSON, default=list)
    endpoint_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )
