from uuid import uuid4

from app.adapters.universal_api_adapter import UniversalAPIAdapter
from app.repositories.enterprise_api_repository import EnterpriseAPIRepository
from app.repositories.execution_repository import ExecutionRepository
from app.utils.serialization import json_safe


class ExecutionService:
    def __init__(
        self,
        enterprise_repository: EnterpriseAPIRepository,
        execution_repository: ExecutionRepository,
        universal_adapter: UniversalAPIAdapter,
    ):
        self.enterprise_repository = enterprise_repository
        self.execution_repository = execution_repository
        self.universal_adapter = universal_adapter

    def execute(self, request_id: str, normalized_execution: dict) -> dict:
        api = self.enterprise_repository.get_by_service_operation(
            normalized_execution.get("service", ""),
            normalized_execution.get("operation", ""),
        )
        if api is None or api.status != "ACTIVE":
            return self._record_failure(
                request_id,
                normalized_execution,
                f"Enterprise API {normalized_execution.get('service')} / {normalized_execution.get('operation')} is not active or registered.",
            )
        try:
            result = self.universal_adapter.execute(api, normalized_execution)
            execution = self.execution_repository.create(
                {
                    "execution_id": f"EXE-{uuid4().hex[:10].upper()}",
                    "request_id": request_id,
                    "executor": self.universal_adapter.executor_name,
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
                "executor": self.universal_adapter.executor_name,
                "api_registry_entry": {
                    "service": api.service_name,
                    "operation": api.operation,
                    "method": api.method,
                    "version": api.version,
                },
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
            return self._record_failure(request_id, normalized_execution, str(exc))

    def simulate(self, request_id: str, normalized_execution: dict) -> dict:
        return {
            "executor": "SimulationOnly",
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

    def _record_failure(self, request_id: str, normalized_execution: dict, message: str) -> dict:
        execution = self.execution_repository.create(
            {
                "execution_id": f"EXE-{uuid4().hex[:10].upper()}",
                "request_id": request_id,
                "executor": self.universal_adapter.executor_name,
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
            "executor": self.universal_adapter.executor_name,
            "enterprise_request": normalized_execution,
            "enterprise_response": {"error": message},
            "status_code": 500,
            "duration_ms": 0,
            "retry_count": 0,
            "execution_id": execution.execution_id,
            "status": "FAILED",
            "business_code": "ENTERPRISE_FAILURE",
        }
