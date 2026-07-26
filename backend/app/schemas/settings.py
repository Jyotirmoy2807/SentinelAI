from pydantic import BaseModel


class SettingsRead(BaseModel):
    app_name: str
    app_env: str
    api_v1_prefix: str
    graph_version: str
    database_url: str
    cors_origins: list[str]
    available_adapters: list[str]
    opa_url: str
    opa_decision_path: str
    opa_policy_bundle_path: str
    audit_sink: str
