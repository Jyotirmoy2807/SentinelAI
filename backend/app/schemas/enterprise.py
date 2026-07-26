from datetime import datetime
from typing import Any

from pydantic import Field

from app.schemas.common import ORMModel


class EnterpriseAPIBase(ORMModel):
    service_name: str
    operation: str
    method: str = "POST"
    base_url: str
    path: str
    authentication_type: str = "NONE"
    authentication_config: dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: int = 30
    retry_count: int = 0
    version: str = "1.0"
    status: str = "ACTIVE"
    required_policies: list[str] = Field(default_factory=list)
    endpoint_metadata: dict[str, Any] = Field(default_factory=dict)


class EnterpriseAPICreate(EnterpriseAPIBase):
    pass


class EnterpriseAPIUpdate(ORMModel):
    service_name: str | None = None
    operation: str | None = None
    method: str | None = None
    base_url: str | None = None
    path: str | None = None
    authentication_type: str | None = None
    authentication_config: dict[str, Any] | None = None
    timeout_seconds: int | None = None
    retry_count: int | None = None
    version: str | None = None
    status: str | None = None
    required_policies: list[str] | None = None
    endpoint_metadata: dict[str, Any] | None = None


class EnterpriseAPIRead(EnterpriseAPIBase):
    id: int
    created_at: datetime
    updated_at: datetime
