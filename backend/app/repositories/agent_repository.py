from sqlalchemy import select

from app.models.agent import Agent
from app.repositories.base import BaseRepository


class AgentRepository(BaseRepository[Agent]):
    model = Agent

    def get_by_passport(self, passport_id: str) -> Agent | None:
        statement = select(Agent).where(Agent.passport_id == passport_id)
        return self.db.scalars(statement).first()

    def list_by_status(self, status: str) -> list[Agent]:
        statement = select(Agent).where(Agent.status == status).order_by(Agent.name)
        return list(self.db.scalars(statement).all())
