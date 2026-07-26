from pydantic import BaseModel, Field


class OpaPolicyRead(BaseModel):
    id: str
    policy_id: str
    name: str
    engine: str = "OPA"
    language: str = "Rego"
    status: str = "ACTIVE"
    path: str
    package: str
    rules: list[str] = Field(default_factory=list)
    content: str
