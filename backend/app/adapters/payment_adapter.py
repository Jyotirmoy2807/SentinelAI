from time import perf_counter

from app.adapters.base import AdapterExecutionResult, EnterpriseAdapter


class PaymentAdapter(EnterpriseAdapter):
    adapter_name = "PaymentAdapter"

    def validate_request(self, request: dict) -> None:
        parameters = request.get("parameters", {})
        if not parameters.get("amount"):
            raise ValueError("Payment amount is required")

    def transform_payload(self, request: dict) -> dict:
        parameters = request.get("parameters", {})
        return {
            "invoiceId": parameters.get("invoice_id"),
            "amount": parameters.get("amount"),
            "currency": parameters.get("currency", "USD"),
            "paymentRail": parameters.get("rail", "ACH"),
        }

    def execute(self, request: dict) -> AdapterExecutionResult:
        started = perf_counter()
        self.validate_request(request)
        payload = self.transform_payload(request)
        return AdapterExecutionResult(
            status="SUCCESS",
            http_code=202,
            business_code="PAYMENT_QUEUED",
            payload={"payment_id": "PAY-MOCK-8841", "queued": True, "amount": payload["amount"]},
            latency_ms=round((perf_counter() - started) * 1000 + 128, 2),
            raw_response={"mock": True, "payload": payload},
        )
