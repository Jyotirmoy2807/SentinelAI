from time import perf_counter

from app.adapters.base import AdapterExecutionResult, EnterpriseAdapter


class InvoiceAdapter(EnterpriseAdapter):
    adapter_name = "InvoiceAdapter"
    SUPPORTED_OPERATIONS = ("create_invoice", "read_invoice")

    def validate_request(self, request: dict) -> None:
        if not request.get("parameters", {}).get("invoice_id"):
            raise ValueError("Invoice ID is required")

    def transform_payload(self, request: dict) -> dict:
        parameters = request.get("parameters", {})
        return {
            "invoiceId": parameters.get("invoice_id"),
            "amount": parameters.get("amount", 0),
            "vendorId": parameters.get("vendor_id", "VND-UNKNOWN"),
        }

    def execute(self, request: dict) -> AdapterExecutionResult:
        started = perf_counter()
        self.validate_request(request)
        payload = self.transform_payload(request)
        return AdapterExecutionResult(
            status="SUCCESS",
            http_code=200,
            business_code="INVOICE_PROCESSED",
            payload={"invoice_id": payload["invoiceId"], "status": "processed"},
            latency_ms=round((perf_counter() - started) * 1000 + 116, 2),
            raw_response={"mock": True, "payload": payload},
        )
