from sqlalchemy import select

from app.models.policy import Policy
from app.repositories.base import BaseRepository


class PolicyRepository(BaseRepository[Policy]):
    model = Policy

    def get_by_policy_id(self, policy_id: str) -> Policy | None:
        statement = select(Policy).where(Policy.policy_id == policy_id)
        return self.db.scalars(statement).first()

    def list_active(self) -> list[Policy]:
        statement = select(Policy).where(Policy.status == "ACTIVE").order_by(Policy.priority)
        return list(self.db.scalars(statement).all())
