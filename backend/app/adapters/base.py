from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AdapterExecutionResult:
    status: str
    http_code: int
    business_code: str
    payload: dict[str, Any]
    latency_ms: float
    retry_count: int = 0
    raw_response: dict[str, Any] = field(default_factory=dict)


class EnterpriseAdapter(ABC):
    adapter_name: str

    @abstractmethod
    def validate_request(self, request: dict[str, Any]) -> None:
        pass

    @abstractmethod
    def transform_payload(self, request: dict[str, Any]) -> dict[str, Any]:
        pass

    @abstractmethod
    def execute(self, request: dict[str, Any]) -> AdapterExecutionResult:
        pass
