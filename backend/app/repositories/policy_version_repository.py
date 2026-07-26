from sqlalchemy import desc, select

from app.models.policy_version import PolicyVersion
from app.repositories.base import BaseRepository


class PolicyVersionRepository(BaseRepository[PolicyVersion]):
    model = PolicyVersion

    def get_by_version_id(self, version_id: str) -> PolicyVersion | None:
        statement = select(PolicyVersion).where(PolicyVersion.version_id == version_id)
        return self.db.scalars(statement).first()

    def list_recent(self, limit: int = 100) -> list[PolicyVersion]:
        statement = select(PolicyVersion).order_by(desc(PolicyVersion.created_at)).limit(limit)
        return list(self.db.scalars(statement).all())
