from sqlalchemy import select

from app.models.compliance_rule import ComplianceRule
from app.repositories.base import BaseRepository


class ComplianceRepository(BaseRepository[ComplianceRule]):
    model = ComplianceRule

    def get_by_rule_id(self, rule_id: str) -> ComplianceRule | None:
        statement = select(ComplianceRule).where(ComplianceRule.rule_id == rule_id)
        return self.db.scalars(statement).first()

    def list_active(self) -> list[ComplianceRule]:
        statement = select(ComplianceRule).where(ComplianceRule.status == "ACTIVE")
        return list(self.db.scalars(statement).all())
