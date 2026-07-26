class RiskService:
    def calculate(self, identity: dict, normalized_execution: dict) -> dict:
        amount = float(normalized_execution.get("amount") or 0)
        operation = normalized_execution.get("operation", "")
        service = normalized_execution.get("service", "")
        trust_score = float(identity.get("trust_score") or 0)
        reputation = float(identity.get("reputation") or 0)

        categorized = self._categorize(service, operation, amount)
        assessed = self._assess(identity, normalized_execution, categorized)
        authorization = self._authorize(assessed["score"])
        monitoring = self._monitor(identity, normalized_execution)
        score = min(round(assessed["score"] + monitoring["anomaly_score"], 2), 100.0)

        return {
            "score": score,
            "level": self._level(score),
            "category": self._level(score),
            "rmf": {
                "categorize": categorized,
                "assess": assessed,
                "authorize": authorization,
                "monitor": monitoring,
            },
            "factors": assessed["factors"] + monitoring["factors"],
            "confidence": 0.92,
            "explanation": f"NIST RMF risk level is {self._level(score)} with score {score}.",
        }

    def _categorize(self, service: str, operation: str, amount: float) -> dict:
        sensitivity = "LOW"
        if service in {"Payment Service", "Refund Service", "Invoice Service"}:
            sensitivity = "HIGH"
        if operation in {"delete_database", "export_personal_data"}:
            sensitivity = "CRITICAL"
        if amount >= 5000:
            sensitivity = "CRITICAL"
        return {
            "api_sensitivity": sensitivity,
            "enterprise_api": service,
            "operation": operation,
            "transaction_amount": amount,
        }

    def _assess(self, identity: dict, normalized_execution: dict, categorized: dict) -> dict:
        amount = float(normalized_execution.get("amount") or 0)
        operation = normalized_execution.get("operation", "")
        trust_score = float(identity.get("trust_score") or 0)
        reputation = float(identity.get("reputation") or 0)
        previous_violations = max(0, int((100 - reputation) / 20))
        customer_sensitivity = self._customer_sensitivity(normalized_execution)

        score = 8.0
        factors = [{"factor": "RMF baseline governance risk", "weight": 8}]
        if amount:
            amount_weight = min(30.0, amount / 250)
            score += amount_weight
            factors.append({"factor": "Transaction risk", "weight": round(amount_weight, 2)})
        sensitivity_weight = {"LOW": 3, "MEDIUM": 8, "HIGH": 16, "CRITICAL": 28}[categorized["api_sensitivity"]]
        score += sensitivity_weight
        factors.append({"factor": f"API sensitivity {categorized['api_sensitivity']}", "weight": sensitivity_weight})
        if trust_score < 75:
            score += 15
            factors.append({"factor": "Trust score below 75", "weight": 15})
        if reputation < 80:
            score += 12
            factors.append({"factor": "Previous violation proxy from low reputation", "weight": 12})
        if any(token in operation for token in ["delete", "refund", "payment", "payout"]):
            score += 14
            factors.append({"factor": f"Sensitive operation {operation}", "weight": 14})
        if customer_sensitivity == "HIGH":
            score += 10
            factors.append({"factor": "Customer sensitivity high", "weight": 10})
        if previous_violations:
            violation_weight = previous_violations * 4
            score += violation_weight
            factors.append({"factor": "Previous violations", "weight": violation_weight})

        return {
            "score": min(round(score, 2), 100.0),
            "transaction_risk": amount,
            "trust_score": trust_score,
            "previous_violations": previous_violations,
            "customer_sensitivity": customer_sensitivity,
            "factors": factors,
        }

    def _authorize(self, score: float) -> dict:
        level = self._level(score)
        return {
            "risk_level": level,
            "authorization_guidance": "OPA may allow" if level in {"LOW", "MEDIUM"} else "OPA should require review",
        }

    def _monitor(self, identity: dict, normalized_execution: dict) -> dict:
        operation = normalized_execution.get("operation", "")
        parameters = str(normalized_execution.get("parameters", {})).lower()
        anomaly_score = 0.0
        factors = []
        if "urgent" in parameters or "override" in parameters:
            anomaly_score += 8
            factors.append({"factor": "Anomalous override language", "weight": 8})
        if identity.get("risk_tier") == "HIGH":
            anomaly_score += 10
            factors.append({"factor": "High-risk agent tier", "weight": 10})
        if operation.startswith("delete"):
            anomaly_score += 15
            factors.append({"factor": "Destructive operation monitor", "weight": 15})
        return {"anomaly_score": anomaly_score, "factors": factors}

    def _customer_sensitivity(self, normalized_execution: dict) -> str:
        parameters = normalized_execution.get("parameters", {})
        tier = str(parameters.get("customer_tier", parameters.get("customerTier", "standard"))).lower()
        if tier in {"vip", "enterprise", "regulated"}:
            return "HIGH"
        return "LOW"

    def _level(self, score: float) -> str:
        category = "LOW"
        if score >= 85:
            category = "CRITICAL"
        elif score >= 70:
            category = "HIGH"
        elif score >= 40:
            category = "MEDIUM"
        return category
