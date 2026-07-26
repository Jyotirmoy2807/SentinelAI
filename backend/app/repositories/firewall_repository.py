from sqlalchemy import select

from app.models.firewall_rule import FirewallRule
from app.repositories.base import BaseRepository


class FirewallRepository(BaseRepository[FirewallRule]):
    model = FirewallRule

    def get_by_rule_id(self, rule_id: str) -> FirewallRule | None:
        statement = select(FirewallRule).where(FirewallRule.rule_id == rule_id)
        return self.db.scalars(statement).first()

    def list_active(self) -> list[FirewallRule]:
        statement = select(FirewallRule).where(FirewallRule.status == "ACTIVE")
        return list(self.db.scalars(statement).all())
