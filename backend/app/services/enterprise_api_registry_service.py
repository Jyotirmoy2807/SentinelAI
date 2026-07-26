from app.models.enterprise_api import EnterpriseAPI
from app.repositories.enterprise_api_repository import EnterpriseAPIRepository


class EnterpriseAPIRegistryService:
    def __init__(self, repository: EnterpriseAPIRepository):
        self.repository = repository

    def list_apis(self) -> list[EnterpriseAPI]:
        return self.repository.list()

    def get_api(self, api_id: int) -> EnterpriseAPI | None:
        return self.repository.get(api_id)

    def get_by_service_name(self, service_name: str) -> EnterpriseAPI | None:
        return self.repository.get_by_service_name(service_name)

    def register_api(self, data: dict) -> EnterpriseAPI:
        api = self.repository.create(data)
        self.repository.db.commit()
        return api

    def update_api(self, api: EnterpriseAPI, data: dict) -> EnterpriseAPI:
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
