from typing import Any

from pydantic import BaseModel, Field


class KPI(BaseModel):
    label: str
    value: str | int | float
    change: str = ""
    tone: str = "info"


class DashboardResponse(BaseModel):
    kpis: list[KPI]
    request_trend: list[dict[str, Any]] = Field(default_factory=list)
    risk_distribution: list[dict[str, Any]] = Field(default_factory=list)
    approval_trend: list[dict[str, Any]] = Field(default_factory=list)
    recent_activity: list[dict[str, Any]] = Field(default_factory=list)
