from typing import Any

from pydantic import BaseModel, Field


class KPI(BaseModel):
    label: str
    value: str | int | float
    change: str = ""
    tone: str = "info"


class DashboardResponse(BaseModel):
    kpis: list[KPI]
    system_health: dict[str, Any] = Field(default_factory=dict)
    recent_executions: list[dict[str, Any]] = Field(default_factory=list)
    recent_audit_events: list[dict[str, Any]] = Field(default_factory=list)
