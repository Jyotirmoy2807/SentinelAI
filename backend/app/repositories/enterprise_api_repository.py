from sqlalchemy import select

from app.models.enterprise_api import EnterpriseAPI
from app.repositories.base import BaseRepository


class EnterpriseAPIRepository(BaseRepository[EnterpriseAPI]):
    model = EnterpriseAPI

    def get_by_service_name(self, service_name: str) -> EnterpriseAPI | None:
        statement = select(EnterpriseAPI).where(EnterpriseAPI.service_name == service_name)
        return self.db.scalars(statement).first()

    def list_active(self) -> list[EnterpriseAPI]:
        statement = select(EnterpriseAPI).where(EnterpriseAPI.status == "ACTIVE").order_by(EnterpriseAPI.service_name)
        return list(self.db.scalars(statement).all())
