from time import perf_counter

from app.adapters.base import AdapterExecutionResult, EnterpriseAdapter


class BookingAdapter(EnterpriseAdapter):
    adapter_name = "BookingAdapter"
    SUPPORTED_OPERATIONS = ("confirm_booking", "cancel_booking")

    def validate_request(self, request: dict) -> None:
        if not request.get("parameters", {}).get("booking_id"):
            raise ValueError("Booking ID is required")

    def transform_payload(self, request: dict) -> dict:
        parameters = request.get("parameters", {})
        return {
            "bookingId": parameters.get("booking_id"),
            "operation": request.get("operation"),
            "requestedChange": parameters.get("change", {}),
        }

    def execute(self, request: dict) -> AdapterExecutionResult:
        started = perf_counter()
        self.validate_request(request)
        payload = self.transform_payload(request)
        return AdapterExecutionResult(
            status="SUCCESS",
            http_code=200,
            business_code="BOOKING_CONFIRMED",
            payload={"booking_id": payload["bookingId"], "status": "confirmed"},
            latency_ms=round((perf_counter() - started) * 1000 + 81, 2),
            raw_response={"mock": True, "payload": payload},
        )
