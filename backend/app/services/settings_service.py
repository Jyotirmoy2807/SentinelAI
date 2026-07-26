from app.adapters.factory import EnterpriseAdapterFactory
from app.core.config import Settings


class SettingsService:
    def __init__(self, settings: Settings, adapter_factory: EnterpriseAdapterFactory):
        self.settings = settings
        self.adapter_factory = adapter_factory

    def read(self) -> dict:
        return {
            "app_name": self.settings.app_name,
            "app_env": self.settings.app_env,
            "api_v1_prefix": self.settings.api_v1_prefix,
            "graph_version": self.settings.graph_version,
            "database_url": self.settings.database_url,
            "cors_origins": self.settings.cors_origins,
            "available_adapters": self.adapter_factory.list_adapters(),
        }
