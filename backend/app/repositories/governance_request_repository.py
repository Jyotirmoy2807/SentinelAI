from sqlalchemy import desc, select

from app.models.governance_request import GovernanceRequest
from app.repositories.base import BaseRepository


class GovernanceRequestRepository(BaseRepository[GovernanceRequest]):
    model = GovernanceRequest

    def get_by_request_id(self, request_id: str) -> GovernanceRequest | None:
        statement = select(GovernanceRequest).where(GovernanceRequest.request_id == request_id)
        return self.db.scalars(statement).first()

    def list_recent(self, limit: int = 50) -> list[GovernanceRequest]:
        statement = select(GovernanceRequest).order_by(desc(GovernanceRequest.created_at)).limit(limit)
        return list(self.db.scalars(statement).all())
