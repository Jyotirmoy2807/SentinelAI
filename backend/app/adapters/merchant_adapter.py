from time import perf_counter

from app.adapters.base import AdapterExecutionResult, EnterpriseAdapter


class MerchantAdapter(EnterpriseAdapter):
    adapter_name = "MerchantAdapter"
    SUPPORTED_OPERATIONS = ("lookup_merchant", "update_merchant")

    def validate_request(self, request: dict) -> None:
        if "merchant_id" not in request.get("parameters", {}):
            raise ValueError("Merchant ID is required")

    def transform_payload(self, request: dict) -> dict:
        parameters = request.get("parameters", {})
        return {
            "merchantId": parameters.get("merchant_id"),
            "operation": request.get("operation"),
            "attributes": parameters.get("attributes", {}),
        }

    def execute(self, request: dict) -> AdapterExecutionResult:
        started = perf_counter()
        self.validate_request(request)
        payload = self.transform_payload(request)
        return AdapterExecutionResult(
            status="SUCCESS",
            http_code=200,
            business_code="MERCHANT_UPDATED",
            payload={"merchant_id": payload["merchantId"], "status": "updated"},
            latency_ms=round((perf_counter() - started) * 1000 + 74, 2),
            raw_response={"mock": True, "payload": payload},
        )
