from sqlalchemy import select

from app.models.budget_policy import BudgetPolicy
from app.repositories.base import BaseRepository


class BudgetPolicyRepository(BaseRepository[BudgetPolicy]):
    model = BudgetPolicy

    def get_by_name(self, name: str) -> BudgetPolicy | None:
        statement = select(BudgetPolicy).where(BudgetPolicy.name == name)
        return self.db.scalars(statement).first()

    def list_ordered(self) -> list[BudgetPolicy]:
        statement = select(BudgetPolicy).order_by(BudgetPolicy.department, BudgetPolicy.name)
        return list(self.db.scalars(statement).all())

    def list_active(self) -> list[BudgetPolicy]:
        statement = select(BudgetPolicy).where(BudgetPolicy.status == "ACTIVE").order_by(BudgetPolicy.department)
        return list(self.db.scalars(statement).all())
