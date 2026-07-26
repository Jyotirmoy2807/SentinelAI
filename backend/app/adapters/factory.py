from app.adapters.base import EnterpriseAdapter
from app.adapters.booking_adapter import BookingAdapter
from app.adapters.invoice_adapter import InvoiceAdapter
from app.adapters.merchant_adapter import MerchantAdapter
from app.adapters.payment_adapter import PaymentAdapter
from app.adapters.refund_adapter import RefundAdapter


class EnterpriseAdapterFactory:
    def __init__(self) -> None:
        self._adapters: dict[str, EnterpriseAdapter] = {
            "BookingAdapter": BookingAdapter(),
            "InvoiceAdapter": InvoiceAdapter(),
            "MerchantAdapter": MerchantAdapter(),
            "PaymentAdapter": PaymentAdapter(),
            "RefundAdapter": RefundAdapter(),
        }

    def get_adapter(self, adapter_name: str) -> EnterpriseAdapter:
        adapter = self._adapters.get(adapter_name)
        if adapter is None:
            raise ValueError(f"No enterprise adapter registered for {adapter_name}")
        return adapter

    def list_adapters(self) -> list[str]:
        return sorted(self._adapters.keys())
