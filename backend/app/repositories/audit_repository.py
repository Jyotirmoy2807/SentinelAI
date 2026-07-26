from sqlalchemy import desc, select

from app.models.audit_log import AuditLog
from app.repositories.base import BaseRepository


class AuditRepository(BaseRepository[AuditLog]):
    model = AuditLog

    def list_by_request(self, request_id: str) -> list[AuditLog]:
        statement = select(AuditLog).where(AuditLog.request_id == request_id).order_by(AuditLog.created_at)
        return list(self.db.scalars(statement).all())

    def list_recent(self, limit: int = 100) -> list[AuditLog]:
        statement = select(AuditLog).order_by(desc(AuditLog.created_at)).limit(limit)
        return list(self.db.scalars(statement).all())
