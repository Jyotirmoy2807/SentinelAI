from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SentinelAI"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./sentinelai.db"
    backend_cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    graph_version: str = "v2"
    opa_url: str = "http://localhost:8181"
    opa_decision_path: str = "/v1/data/sentinelai/governance/decision"
    opa_policy_bundle_path: str = "./app/policies/rego"
    audit_sink: str = "sqlite-splunk"
    request_timeout_seconds: int = Field(default=30, ge=1)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
