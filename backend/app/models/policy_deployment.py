from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.utils.time import utc_now


class PolicyDeployment(Base):
    __tablename__ = "policy_deployments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    deployment_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(40), default="PENDING", index=True)
    message: Mapped[str] = mapped_column(Text, default="")
    checksum: Mapped[str] = mapped_column(String(128), default="")
    opa_fmt_status: Mapped[str] = mapped_column(String(40), default="NOT_RUN")
    opa_check_status: Mapped[str] = mapped_column(String(40), default="NOT_RUN")
    opa_reload_status: Mapped[str] = mapped_column(String(80), default="NOT_RUN")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)
