from app.models.enterprise_api import EnterpriseAPI
from app.repositories.enterprise_api_repository import EnterpriseAPIRepository


class EnterpriseAPIRegistryService:
    STATUSES = {"ACTIVE", "INACTIVE", "MAINTENANCE", "DELETED"}

    def __init__(self, repository: EnterpriseAPIRepository, adapter_factory, governance_policy_repository=None):
        self.repository = repository
        self.adapter_factory = adapter_factory
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

    def adapter_metadata(self) -> list[dict]:
        return self.adapter_factory.list_adapter_metadata()

    def _normalize_and_validate(self, data: dict) -> dict:
        adapter = data.get("adapter")
        if data.get("status") not in self.STATUSES:
            raise ValueError(f"Unsupported enterprise API status: {data.get('status')}")
        supported = self.adapter_factory.supported_operations(adapter)
        requested = data.get("supported_operations") or supported
        invalid = sorted(set(requested) - set(supported))
        if invalid:
            raise ValueError(f"Unsupported operations for {adapter}: {', '.join(invalid)}")
        if self.governance_policy_repository:
            policy_ids = {policy.policy_id for policy in self.governance_policy_repository.list_ordered()}
            unknown_policies = sorted(set(data.get("required_policies", [])) - policy_ids)
            if unknown_policies:
                raise ValueError(f"Unknown governance policies: {', '.join(unknown_policies)}")
        data["supported_operations"] = requested
        return data

    def _to_dict(self, api: EnterpriseAPI) -> dict:
        return {
            "service_name": api.service_name,
            "adapter": api.adapter,
            "version": api.version,
            "status": api.status,
            "supported_operations": api.supported_operations,
            "required_policies": api.required_policies,
            "endpoint_metadata": api.endpoint_metadata,
        }
