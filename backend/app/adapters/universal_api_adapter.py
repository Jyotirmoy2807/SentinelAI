from __future__ import annotations

from base64 import b64encode
from dataclasses import dataclass
import json
from time import perf_counter
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from app.models.enterprise_api import EnterpriseAPI
from app.utils.serialization import json_safe


@dataclass(frozen=True)
class UniversalAPIResult:
    status: str
    http_code: int
    business_code: str
    payload: dict[str, Any]
    latency_ms: float
    retry_count: int = 0


class UniversalAPIAdapter:
    executor_name = "UniversalAPIAdapter"

    def execute(self, api: EnterpriseAPI, normalized_execution: dict[str, Any]) -> UniversalAPIResult:
        started = perf_counter()
        parameters = normalized_execution.get("parameters") or {}
        url = self._build_url(api.base_url, api.path)

        if self._is_mock_endpoint(url):
            return UniversalAPIResult(
                status="COMPLETED",
                http_code=200,
                business_code="MOCK_COMPLETED",
                payload={
                    "service": api.service_name,
                    "operation": api.operation,
                    "method": api.method,
                    "mock": True,
                    "accepted": True,
                    "parameters": json_safe(parameters),
                },
                latency_ms=round((perf_counter() - started) * 1000, 2),
                retry_count=0,
            )

        attempts = max(1, int(api.retry_count or 0) + 1)
        last_error = ""
        for attempt in range(attempts):
            try:
                response = self._send(api, url, parameters)
                return UniversalAPIResult(
                    status="COMPLETED" if response["status_code"] < 400 else "FAILED",
                    http_code=response["status_code"],
                    business_code="HTTP_COMPLETED",
                    payload=response["payload"],
                    latency_ms=round((perf_counter() - started) * 1000, 2),
                    retry_count=attempt,
                )
            except (HTTPError, URLError, TimeoutError, OSError) as exc:
                last_error = str(exc)

        return UniversalAPIResult(
            status="FAILED",
            http_code=502,
            business_code="UPSTREAM_UNAVAILABLE",
            payload={"error": last_error or "Enterprise API invocation failed."},
            latency_ms=round((perf_counter() - started) * 1000, 2),
            retry_count=max(0, attempts - 1),
        )

    def _send(self, api: EnterpriseAPI, url: str, parameters: dict[str, Any]) -> dict[str, Any]:
        method = api.method.upper()
        headers = {"Accept": "application/json"}
        body = None
        if method == "GET" and parameters:
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}{urlencode(parameters, doseq=True)}"
        else:
            body = json.dumps(parameters).encode("utf-8")
            headers["Content-Type"] = "application/json"

        headers.update(self._auth_headers(api.authentication_type, api.authentication_config or {}))
        request = Request(url=url, data=body, headers=headers, method=method)
        with urlopen(request, timeout=int(api.timeout_seconds or 30)) as response:
            raw = response.read().decode("utf-8")
            return {"status_code": response.status, "payload": self._decode_payload(raw)}

    def _auth_headers(self, auth_type: str, config: dict[str, Any]) -> dict[str, str]:
        normalized = (auth_type or "NONE").upper()
        if normalized == "API_KEY":
            header_name = config.get("headerName") or config.get("header_name") or "X-API-Key"
            api_key = config.get("apiKey") or config.get("api_key") or ""
            return {header_name: str(api_key)} if api_key else {}
        if normalized in {"BEARER_TOKEN", "OAUTH2"}:
            token = config.get("token") or config.get("accessToken") or config.get("access_token") or ""
            return {"Authorization": f"Bearer {token}"} if token else {}
        if normalized == "BASIC":
            username = str(config.get("username") or "")
            password = str(config.get("password") or "")
            if not username:
                return {}
            encoded = b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
            return {"Authorization": f"Basic {encoded}"}
        return {}

    def _build_url(self, base_url: str, path: str) -> str:
        return f"{str(base_url).rstrip('/')}/{str(path).lstrip('/')}"

    def _is_mock_endpoint(self, url: str) -> bool:
        parsed = urlparse(url)
        return parsed.scheme == "mock" or parsed.hostname in {"mock.local", "sentinelai.mock"}

    def _decode_payload(self, raw: str) -> dict[str, Any]:
        if not raw:
            return {}
        try:
            decoded = json.loads(raw)
        except json.JSONDecodeError:
            return {"body": raw}
        return decoded if isinstance(decoded, dict) else {"data": decoded}
