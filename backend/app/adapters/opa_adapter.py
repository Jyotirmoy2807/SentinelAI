import json
from dataclasses import dataclass
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class OpaEvaluationResult:
    decision: str
    matched_policy: str
    reasons: list[str]
    raw_result: dict[str, Any]
    opa_url: str


class OpaPolicyAdapter:
    def __init__(self, base_url: str, decision_path: str, timeout_seconds: int = 5):
        self.base_url = base_url.rstrip("/")
        self.decision_path = decision_path
        self.timeout_seconds = timeout_seconds

    def evaluate(self, policy_input: dict[str, Any]) -> OpaEvaluationResult:
        url = f"{self.base_url}{self.decision_path}"
        request = Request(
            url,
            data=json.dumps({"input": policy_input}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8"))
        except (OSError, URLError, TimeoutError) as exc:
            return OpaEvaluationResult(
                decision="DENY",
                matched_policy="OPA_UNAVAILABLE",
                reasons=[f"OPA is unavailable at {url}; governance failed closed. {exc}"],
                raw_result={"error": str(exc)},
                opa_url=url,
            )

        result = body.get("result") or {}
        reasons = result.get("reasons") or result.get("reason") or []
        if isinstance(reasons, str):
            reasons = [reasons]
        return OpaEvaluationResult(
            decision=str(result.get("decision", "DENY")).upper(),
            matched_policy=result.get("matched_policy", "sentinelai/governance"),
            reasons=reasons,
            raw_result=result,
            opa_url=url,
        )
