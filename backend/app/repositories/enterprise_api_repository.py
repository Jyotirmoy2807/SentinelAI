from __future__ import annotations

from sqlalchemy import func, select

from app.models.enterprise_api import EnterpriseAPI
from app.repositories.base import BaseRepository


class EnterpriseAPIRepository(BaseRepository[EnterpriseAPI]):
    model = EnterpriseAPI

    def list(self, skip: int = 0, limit: int = 100) -> list[EnterpriseAPI]:
        statement = select(EnterpriseAPI).order_by(EnterpriseAPI.service_name, EnterpriseAPI.operation).offset(skip).limit(limit)
        return list(self.db.scalars(statement).all())

    def get_by_service_name(self, service_name: str) -> EnterpriseAPI | None:
        statement = select(EnterpriseAPI).where(EnterpriseAPI.service_name == service_name)
        return self.db.scalars(statement).first()

    def get_by_service_operation(self, service_name: str, operation: str) -> EnterpriseAPI | None:
        statement = select(EnterpriseAPI).where(
            EnterpriseAPI.service_name == service_name,
            EnterpriseAPI.operation == operation,
        )
        api = self.db.scalars(statement).first()
        if api:
            return api
        fallback = select(EnterpriseAPI).where(
            func.lower(EnterpriseAPI.service_name) == service_name.lower(),
            func.lower(EnterpriseAPI.operation) == operation.lower(),
        )
        return self.db.scalars(fallback).first()

    def list_active(self) -> list[EnterpriseAPI]:
        statement = select(EnterpriseAPI).where(EnterpriseAPI.status == "ACTIVE").order_by(EnterpriseAPI.service_name, EnterpriseAPI.operation)
        return list(self.db.scalars(statement).all())
