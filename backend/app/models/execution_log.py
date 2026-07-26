from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.utils.time import utc_now


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    execution_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    request_id: Mapped[str] = mapped_column(String(80), index=True)
    adapter: Mapped[str] = mapped_column(String(80), default="")
    enterprise_status: Mapped[str] = mapped_column(String(80), default="")
    response_code: Mapped[str] = mapped_column(String(32), default="")
    latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    retries: Mapped[int] = mapped_column(Integer, default=0)
    request_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    response_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
