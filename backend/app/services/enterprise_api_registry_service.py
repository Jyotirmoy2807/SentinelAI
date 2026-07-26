from app.models.enterprise_api import EnterpriseAPI
from app.repositories.enterprise_api_repository import EnterpriseAPIRepository


class EnterpriseAPIRegistryService:
    STATUSES = {"ACTIVE", "INACTIVE", "MAINTENANCE", "DELETED"}
    METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}
    AUTHENTICATION_TYPES = {"NONE", "API_KEY", "BEARER_TOKEN", "BASIC", "OAUTH2"}

    def __init__(self, repository: EnterpriseAPIRepository, governance_policy_repository=None):
        self.repository = repository
        self.governance_policy_repository = governance_policy_repository

    def list_apis(self) -> list[EnterpriseAPI]:
        return self.repository.list()

    def get_api(self, api_id: int) -> EnterpriseAPI | None:
        return self.repository.get(api_id)

    def get_by_service_name(self, service_name: str) -> EnterpriseAPI | None:
        return self.repository.get_by_service_name(service_name)

    def register_api(self, data: dict) -> EnterpriseAPI:
        data = self._normalize_and_validate(data)
        api = self.repository.create(data)
        self.repository.db.commit()
        return api

    def update_api(self, api: EnterpriseAPI, data: dict) -> EnterpriseAPI:
        data = self._normalize_and_validate({**self._to_dict(api), **data})
        data.pop("id", None)
        updated = self.repository.update(api, data)
        self.repository.db.commit()
        return updated

    def set_status(self, api: EnterpriseAPI, status: str) -> EnterpriseAPI:
        updated = self.repository.update(api, {"status": status})
        self.repository.db.commit()
        return updated

    def delete_api(self, api: EnterpriseAPI) -> EnterpriseAPI:
        updated = self.repository.update(api, {"status": "DELETED"})
        self.repository.db.commit()
        return updated

    def lookups(self) -> dict:
        apis = self.repository.list()
        return {
            "services": sorted({api.service_name for api in apis if api.status != "DELETED"}),
            "methods": sorted(self.METHODS),
            "authentication_types": sorted(self.AUTHENTICATION_TYPES),
            "statuses": sorted(self.STATUSES - {"DELETED"}),
        }

    def _normalize_and_validate(self, data: dict) -> dict:
        data["service_name"] = str(data.get("service_name") or "").strip()
        data["operation"] = str(data.get("operation") or "").strip()
        data["method"] = str(data.get("method") or "POST").upper()
        data["authentication_type"] = str(data.get("authentication_type") or "NONE").upper()
        data["status"] = str(data.get("status") or "ACTIVE").upper()
        data["path"] = str(data.get("path") or "").strip() or "/"
        data["base_url"] = str(data.get("base_url") or "").strip()
        data["version"] = str(data.get("version") or "1.0").strip()
        data["timeout_seconds"] = int(data.get("timeout_seconds") or 30)
        data["retry_count"] = int(data.get("retry_count") or 0)
        data["authentication_config"] = data.get("authentication_config") or {}
        data["required_policies"] = data.get("required_policies") or []
        data["endpoint_metadata"] = data.get("endpoint_metadata") or {}

        if not data["service_name"]:
            raise ValueError("Service name is required.")
        if not data["operation"]:
            raise ValueError("Operation is required.")
        if not data["base_url"]:
            raise ValueError("Base URL is required.")
        if data["status"] not in self.STATUSES:
            raise ValueError(f"Unsupported enterprise API status: {data['status']}")
        if data["method"] not in self.METHODS:
            raise ValueError(f"Unsupported HTTP method: {data['method']}")
        if data["authentication_type"] not in self.AUTHENTICATION_TYPES:
            raise ValueError(f"Unsupported authentication type: {data['authentication_type']}")
        if data["timeout_seconds"] < 1 or data["timeout_seconds"] > 120:
            raise ValueError("Timeout must be between 1 and 120 seconds.")
        if data["retry_count"] < 0 or data["retry_count"] > 5:
            raise ValueError("Retry count must be between 0 and 5.")

        if self.governance_policy_repository:
            policy_ids = {policy.policy_id for policy in self.governance_policy_repository.list_ordered()}
            unknown_policies = sorted(set(data.get("required_policies", [])) - policy_ids)
            if unknown_policies:
                raise ValueError(f"Unknown governance policies: {', '.join(unknown_policies)}")
        existing = self.repository.get_by_service_operation(data["service_name"], data["operation"])
        if existing and existing.id != data.get("id"):
            raise ValueError(f"API operation already registered for {data['service_name']} / {data['operation']}.")
        return data

    def _to_dict(self, api: EnterpriseAPI) -> dict:
        return {
            "id": api.id,
            "service_name": api.service_name,
            "operation": api.operation,
            "method": api.method,
            "base_url": api.base_url,
            "path": api.path,
            "authentication_type": api.authentication_type,
            "authentication_config": api.authentication_config,
            "timeout_seconds": api.timeout_seconds,
            "retry_count": api.retry_count,
            "version": api.version,
            "status": api.status,
            "required_policies": api.required_policies,
            "endpoint_metadata": api.endpoint_metadata,
        }
