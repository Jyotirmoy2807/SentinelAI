from sqlalchemy import select

from app.models.governance_decision import GovernanceDecision
from app.repositories.base import BaseRepository


class GovernanceDecisionRepository(BaseRepository[GovernanceDecision]):
    model = GovernanceDecision

    def list_by_request(self, request_id: str) -> list[GovernanceDecision]:
        statement = select(GovernanceDecision).where(GovernanceDecision.request_id == request_id).order_by(
            GovernanceDecision.created_at
        )
        return list(self.db.scalars(statement).all())
