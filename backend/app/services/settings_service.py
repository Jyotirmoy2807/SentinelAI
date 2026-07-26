from app.adapters.factory import EnterpriseAdapterFactory
from app.core.config import Settings


class SettingsService:
    def __init__(self, settings: Settings, adapter_factory: EnterpriseAdapterFactory, services=None):
        self.settings = settings
        self.adapter_factory = adapter_factory
        self.services = services

    def read(self) -> dict:
        return {
            "app_name": self.settings.app_name,
            "app_env": self.settings.app_env,
            "api_v1_prefix": self.settings.api_v1_prefix,
            "graph_version": self.settings.graph_version,
            "database_url": self.settings.database_url,
            "cors_origins": self.settings.cors_origins,
            "available_adapters": self.adapter_factory.list_adapters(),
            "adapter_catalog": self.adapter_factory.list_adapter_metadata(),
            "opa_url": self.settings.opa_url,
            "opa_decision_path": self.settings.opa_decision_path,
            "opa_policy_bundle_path": self.settings.opa_policy_bundle_path,
            "opa_cli_path": self.settings.opa_cli_path,
            "audit_sink": self.settings.audit_sink,
            "log_level": self.settings.log_level,
        }

    def lookups(self) -> dict:
        policies = self.services.policies.list_governance_policies() if self.services else []
        budgets = self.services.policies.list_budget_policies() if self.services else []
        agents = self.services.agents.list_agents() if self.services else []
        enterprise = self.services.enterprise_registry.list_apis() if self.services else []
        policy_lookups = self.services.policies.lookups() if self.services else {}
        return {
            **policy_lookups,
            "adapters": self.adapter_factory.list_adapter_metadata(),
            "enterprise_apis": [{"id": item.id, "service_name": item.service_name, "adapter": item.adapter, "supported_operations": item.supported_operations} for item in enterprise],
            "governance_policies": [{"id": item.id, "policy_id": item.policy_id, "name": item.name, "enabled": item.enabled} for item in policies],
            "budget_policies": [{"id": item.id, "name": item.name, "department": item.department, "status": item.status} for item in budgets],
            "agent_passports": [{"id": item.id, "passport_id": item.passport_id, "name": item.name, "department": item.department} for item in agents],
            "versions": sorted({item.version for item in agents} | {item.version for item in enterprise}),
            "agent_statuses": ["ACTIVE", "SUSPENDED", "BLOCKED", "DELETED"],
            "risk_tiers": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
        }
