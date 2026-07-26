from datetime import datetime
from typing import Any

from pydantic import Field

from app.schemas.common import ORMModel


class EnterpriseAPIBase(ORMModel):
    service_name: str
    adapter: str
    version: str = "1.0"
    status: str = "ACTIVE"
    supported_operations: list[str] = Field(default_factory=list)
    required_policies: list[str] = Field(default_factory=list)
    endpoint_metadata: dict[str, Any] = Field(default_factory=dict)


class EnterpriseAPICreate(EnterpriseAPIBase):
    pass


class EnterpriseAPIUpdate(ORMModel):
    service_name: str | None = None
    adapter: str | None = None
    version: str | None = None
    status: str | None = None
    supported_operations: list[str] | None = None
    required_policies: list[str] | None = None
    endpoint_metadata: dict[str, Any] | None = None


class EnterpriseAPIRead(EnterpriseAPIBase):
    id: int
    created_at: datetime
    updated_at: datetime
