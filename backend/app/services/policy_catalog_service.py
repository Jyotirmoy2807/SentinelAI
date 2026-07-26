from pathlib import Path


class PolicyCatalogService:
    def __init__(self, policy_directory: str):
        self.policy_directory = Path(policy_directory)

    def list_policies(self) -> list[dict]:
        if not self.policy_directory.exists():
            return []
        policies = []
        for path in sorted(self.policy_directory.glob("*.rego")):
            content = path.read_text(encoding="utf-8")
            policies.append(
                {
                    "id": path.stem,
                    "policy_id": path.stem,
                    "name": path.stem.replace("_", " ").replace("-", " ").title(),
                    "engine": "OPA",
                    "language": "Rego",
                    "status": "ACTIVE",
                    "path": str(path),
                    "package": self._extract_package(content),
                    "rules": self._extract_rules(content),
                    "content": content,
                }
            )
        return policies

    def count_active(self) -> int:
        return len(self.list_policies())

    def _extract_package(self, content: str) -> str:
        for line in content.splitlines():
            if line.strip().startswith("package "):
                return line.strip().replace("package ", "", 1)
        return "unknown"

    def _extract_rules(self, content: str) -> list[str]:
        rules = []
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.endswith("{") and not stripped.startswith(("package", "#")):
                rules.append(stripped[:-1].strip())
        return rules
