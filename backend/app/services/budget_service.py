from app.models.budget import BudgetProfile
from app.repositories.budget_repository import BudgetRepository


class BudgetService:
    def __init__(self, repository: BudgetRepository):
        self.repository = repository

    def list_profiles(self) -> list[BudgetProfile]:
        return self.repository.list()

    def get_profile(self, profile_id: int) -> BudgetProfile | None:
        return self.repository.get(profile_id)

    def create_profile(self, data: dict) -> BudgetProfile:
        profile = self.repository.create(data)
        self.repository.db.commit()
        return profile

    def update_profile(self, profile: BudgetProfile, data: dict) -> BudgetProfile:
        updated = self.repository.update(profile, data)
        self.repository.db.commit()
        return updated

    def delete_profile(self, profile: BudgetProfile) -> BudgetProfile:
        updated = self.repository.update(profile, {"status": "DELETED"})
        self.repository.db.commit()
        return updated

    def validate(self, identity: dict, normalized_execution: dict) -> dict:
        amount = float(normalized_execution.get("amount") or 0)
        profile_name = identity.get("budget_profile") or "Standard"
        profile = self.repository.get_by_name(profile_name)
        if profile is None or profile.status != "ACTIVE":
            return {
                "decision": "DENY",
                "budget_profile": profile_name,
                "budget_consumed": 0,
                "remaining_budget": 0,
                "transaction_amount": amount,
                "threshold": 0,
                "reasons": [f"Budget profile {profile_name} is not active or does not exist."],
            }
        remaining_daily = profile.daily_limit - profile.spent_today
        remaining_monthly = profile.monthly_limit - profile.spent_month
        reasons = []
        if amount > profile.transaction_limit:
            reasons.append(f"Amount {amount} exceeds transaction limit {profile.transaction_limit}.")
        if amount > remaining_daily:
            reasons.append(f"Amount {amount} exceeds remaining daily budget {remaining_daily}.")
        if amount > remaining_monthly:
            reasons.append(f"Amount {amount} exceeds remaining monthly budget {remaining_monthly}.")
        if reasons:
            return {
                "decision": "DENY",
                "budget_profile": profile.name,
                "budget_consumed": profile.spent_today,
                "remaining_budget": min(remaining_daily, remaining_monthly),
                "transaction_amount": amount,
                "threshold": profile.transaction_limit,
                "approval_threshold": profile.approval_threshold,
                "reasons": reasons,
            }
        decision = "REQUIRE_APPROVAL" if amount >= profile.approval_threshold and amount > 0 else "ALLOW"
        return {
            "decision": decision,
            "budget_profile": profile.name,
            "budget_consumed": profile.spent_today,
            "remaining_budget": min(remaining_daily, remaining_monthly),
            "transaction_amount": amount,
            "threshold": profile.transaction_limit,
            "approval_threshold": profile.approval_threshold,
            "reasons": (
                [f"Amount {amount} exceeds approval threshold {profile.approval_threshold}."]
                if decision == "REQUIRE_APPROVAL"
                else ["Budget limits are available."]
            ),
        }
