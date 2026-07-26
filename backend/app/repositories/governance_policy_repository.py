from sqlalchemy import desc, select

from app.models.governance_policy import GovernancePolicy
from app.repositories.base import BaseRepository


class GovernancePolicyRepository(BaseRepository[GovernancePolicy]):
    model = GovernancePolicy

    def get_by_policy_id(self, policy_id: str) -> GovernancePolicy | None:
        statement = select(GovernancePolicy).where(GovernancePolicy.policy_id == policy_id)
        return self.db.scalars(statement).first()

    def list_ordered(self) -> list[GovernancePolicy]:
        statement = select(GovernancePolicy).order_by(desc(GovernancePolicy.priority), GovernancePolicy.policy_id)
        return list(self.db.scalars(statement).all())

    def list_active(self) -> list[GovernancePolicy]:
        statement = select(GovernancePolicy).where(GovernancePolicy.enabled.is_(True)).order_by(desc(GovernancePolicy.priority))
        return list(self.db.scalars(statement).all())
