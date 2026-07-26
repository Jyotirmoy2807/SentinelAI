from uuid import uuid4

from app.adapters.factory import EnterpriseAdapterFactory
from app.repositories.enterprise_api_repository import EnterpriseAPIRepository
from app.repositories.execution_repository import ExecutionRepository
from app.utils.serialization import json_safe


class ExecutionService:
    def __init__(
        self,
        enterprise_repository: EnterpriseAPIRepository,
        execution_repository: ExecutionRepository,
        adapter_factory: EnterpriseAdapterFactory,
    ):
        self.enterprise_repository = enterprise_repository
        self.execution_repository = execution_repository
        self.adapter_factory = adapter_factory

    def execute(self, request_id: str, normalized_execution: dict) -> dict:
        api = self.enterprise_repository.get_by_service_name(normalized_execution.get("service", ""))
        if api is None or api.status != "ACTIVE":
            return self._record_failure(
                request_id,
                "UNREGISTERED",
                normalized_execution,
                f"Enterprise API {normalized_execution.get('service')} is not active or registered.",
            )
        try:
            adapter = self.adapter_factory.get_adapter(api.adapter)
            result = adapter.execute(normalized_execution)
            execution = self.execution_repository.create(
                {
                    "execution_id": f"EXE-{uuid4().hex[:10].upper()}",
                    "request_id": request_id,
                    "adapter": api.adapter,
                    "enterprise_status": result.status,
                    "response_code": str(result.http_code),
                    "latency_ms": result.latency_ms,
                    "retries": result.retry_count,
                    "request_payload": json_safe(normalized_execution),
                    "response_payload": json_safe(result.payload),
                }
            )
            self.execution_repository.db.commit()
            return {
                "adapter_used": api.adapter,
                "enterprise_request": normalized_execution,
                "enterprise_response": result.payload,
                "status_code": result.http_code,
                "duration_ms": result.latency_ms,
                "retry_count": result.retry_count,
                "execution_id": execution.execution_id,
                "status": result.status,
                "business_code": result.business_code,
            }
        except Exception as exc:
            return self._record_failure(request_id, api.adapter, normalized_execution, str(exc))

    def simulate(self, request_id: str, normalized_execution: dict) -> dict:
        return {
            "adapter_used": "SimulationAdapter",
            "enterprise_request": normalized_execution,
            "enterprise_response": {
                "simulated": True,
                "message": "Enterprise execution was intentionally skipped for simulation mode.",
            },
            "status_code": 200,
            "duration_ms": 0,
            "retry_count": 0,
            "execution_id": f"SIM-{request_id}",
            "status": "SIMULATED",
            "business_code": "SIMULATION_ONLY",
        }

    def list_by_request(self, request_id: str) -> list:
        return self.execution_repository.list_by_request(request_id)

    def _record_failure(self, request_id: str, adapter: str, normalized_execution: dict, message: str) -> dict:
        execution = self.execution_repository.create(
            {
                "execution_id": f"EXE-{uuid4().hex[:10].upper()}",
                "request_id": request_id,
                "adapter": adapter,
                "enterprise_status": "FAILED",
                "response_code": "500",
                "latency_ms": 0,
                "retries": 0,
                "request_payload": json_safe(normalized_execution),
                "response_payload": {"error": message},
            }
        )
        self.execution_repository.db.commit()
        return {
            "adapter_used": adapter,
            "enterprise_request": normalized_execution,
            "enterprise_response": {"error": message},
            "status_code": 500,
            "duration_ms": 0,
            "retry_count": 0,
            "execution_id": execution.execution_id,
            "status": "FAILED",
            "business_code": "ENTERPRISE_FAILURE",
        }
