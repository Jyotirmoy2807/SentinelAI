from sqlalchemy import desc, select

from app.models.policy_deployment import PolicyDeployment
from app.repositories.base import BaseRepository


class PolicyDeploymentRepository(BaseRepository[PolicyDeployment]):
    model = PolicyDeployment

    def latest(self) -> PolicyDeployment | None:
        statement = select(PolicyDeployment).order_by(desc(PolicyDeployment.created_at)).limit(1)
        return self.db.scalars(statement).first()
