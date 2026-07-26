from sqlalchemy import select

from app.models.budget import BudgetProfile
from app.repositories.base import BaseRepository


class BudgetRepository(BaseRepository[BudgetProfile]):
    model = BudgetProfile

    def get_by_name(self, name: str) -> BudgetProfile | None:
        statement = select(BudgetProfile).where(BudgetProfile.name == name)
        return self.db.scalars(statement).first()
