from sqlalchemy import desc, select

from app.models.approval import Approval
from app.repositories.base import BaseRepository


class ApprovalRepository(BaseRepository[Approval]):
    model = Approval

    def get_by_approval_id(self, approval_id: str) -> Approval | None:
        statement = select(Approval).where(Approval.approval_id == approval_id)
        return self.db.scalars(statement).first()

    def get_by_request_id(self, request_id: str) -> Approval | None:
        statement = select(Approval).where(Approval.request_id == request_id).order_by(desc(Approval.created_at))
        return self.db.scalars(statement).first()

    def list_pending(self) -> list[Approval]:
        statement = select(Approval).where(Approval.status == "PENDING").order_by(desc(Approval.created_at))
        return list(self.db.scalars(statement).all())

    def list_recent(self, limit: int = 100) -> list[Approval]:
        statement = select(Approval).order_by(desc(Approval.created_at)).limit(limit)
        return list(self.db.scalars(statement).all())
