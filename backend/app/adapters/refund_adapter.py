from time import perf_counter

from app.adapters.base import AdapterExecutionResult, EnterpriseAdapter


class RefundAdapter(EnterpriseAdapter):
    adapter_name = "RefundAdapter"
    SUPPORTED_OPERATIONS = ("issue_refund", "read_refund")

    def validate_request(self, request: dict) -> None:
        if "amount" not in request.get("parameters", {}):
            raise ValueError("Refund amount is required")

    def transform_payload(self, request: dict) -> dict:
        parameters = request.get("parameters", {})
        return {
            "merchantId": parameters.get("merchant_id", "MER-UNKNOWN"),
            "amount": parameters.get("amount", 0),
            "reason": parameters.get("reason", "Governed refund"),
            "source": "SentinelAI",
        }

    def execute(self, request: dict) -> AdapterExecutionResult:
        started = perf_counter()
        self.validate_request(request)
        payload = self.transform_payload(request)
        raw = {"refund_id": "RFND-MOCK-1042", "status": "accepted", "payload": payload}
        return AdapterExecutionResult(
            status="SUCCESS",
            http_code=200,
            business_code="REFUND_ACCEPTED",
            payload={"refund_id": raw["refund_id"], "message": "Refund accepted by mock Refund Service"},
            latency_ms=round((perf_counter() - started) * 1000 + 92, 2),
            raw_response=raw,
        )
