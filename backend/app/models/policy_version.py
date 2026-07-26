from datetime import datetime

from sqlalchemy import DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.utils.time import utc_now


class PolicyVersion(Base):
    __tablename__ = "policy_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    version_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    resource_type: Mapped[str] = mapped_column(String(60), index=True)
    resource_key: Mapped[str] = mapped_column(String(160), index=True)
    action: Mapped[str] = mapped_column(String(60), default="SNAPSHOT")
    snapshot: Mapped[dict] = mapped_column(JSON, default=dict)
    generated_rego: Mapped[str] = mapped_column(Text, default="")
    created_by: Mapped[str] = mapped_column(String(160), default="system")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)
