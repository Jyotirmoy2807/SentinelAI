from pydantic import BaseModel, Field


class OpaPolicyCreate(BaseModel):
    policy_id: str = Field(min_length=3, max_length=80, pattern=r"^[a-zA-Z0-9_-]+$")
    name: str = Field(min_length=2, max_length=120)
    content: str = Field(min_length=20)


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
