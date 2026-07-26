from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class GovernanceRequestMetadata(BaseModel):
    passport_id: str = Field(alias="passportId")
    agent_version: str | None = Field(default=None, alias="agentVersion")
    idempotency_key: str | None = Field(default=None, alias="idempotencyKey")

    model_config = ConfigDict(populate_by_name=True)


class GovernanceExecutionIntent(BaseModel):
    service: str
    operation: str
    parameters: dict[str, Any] = Field(default_factory=dict)


class GovernanceRequest(BaseModel):
    metadata: GovernanceRequestMetadata
    execution: GovernanceExecutionIntent


class NodeEvent(BaseModel):
    request_id: str
    node: str
    status: str
    timestamp: datetime
    duration_ms: float = 0.0
    payload: dict[str, Any] = Field(default_factory=dict)


class GovernanceResponse(BaseModel):
    metadata: dict[str, Any]
    governance: dict[str, Any]
    result: dict[str, Any] | None = None
    explainability: dict[str, Any] = Field(default_factory=dict)
    state: dict[str, Any] = Field(default_factory=dict)


class SimulationSample(BaseModel):
    id: str
    name: str
    description: str
    request: GovernanceRequest
