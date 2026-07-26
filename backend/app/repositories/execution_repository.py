from sqlalchemy import desc, select

from app.models.execution_log import ExecutionLog
from app.repositories.base import BaseRepository


class ExecutionRepository(BaseRepository[ExecutionLog]):
    model = ExecutionLog

    def list_by_request(self, request_id: str) -> list[ExecutionLog]:
        statement = select(ExecutionLog).where(ExecutionLog.request_id == request_id).order_by(ExecutionLog.executed_at)
        return list(self.db.scalars(statement).all())

    def list_recent(self, limit: int = 100) -> list[ExecutionLog]:
        statement = select(ExecutionLog).order_by(desc(ExecutionLog.executed_at)).limit(limit)
        return list(self.db.scalars(statement).all())
