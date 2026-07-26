class NormalizationService:
    def normalize(self, raw_request: dict) -> dict:
        metadata = raw_request.get("metadata", {})
        execution = raw_request.get("execution", {})
        service = self._normalize_label(execution.get("service", ""))
        operation = self._normalize_operation(execution.get("operation", ""))
        parameters = execution.get("parameters") or {}
        return {
            "passport_id": metadata.get("passportId") or metadata.get("passport_id"),
            "agent_version": metadata.get("agentVersion") or metadata.get("agent_version"),
            "idempotency_key": metadata.get("idempotencyKey") or metadata.get("idempotency_key"),
            "service": service,
            "operation": operation,
            "parameters": parameters,
            "amount": self._extract_amount(parameters),
        }

    def _normalize_label(self, value: str) -> str:
        return str(value or "").strip()

    def _normalize_operation(self, value: str) -> str:
        return str(value or "").strip()

    def _extract_amount(self, parameters: dict) -> float:
        amount = parameters.get("amount") or parameters.get("total") or 0
        try:
            return float(amount)
        except (TypeError, ValueError):
            return 0.0
