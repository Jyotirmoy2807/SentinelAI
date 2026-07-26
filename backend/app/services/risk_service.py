class RiskService:
    def calculate(self, identity: dict, normalized_execution: dict) -> dict:
        amount = float(normalized_execution.get("amount") or 0)
        operation = normalized_execution.get("operation", "")
        service = normalized_execution.get("service", "")
        trust_score = float(identity.get("trust_score") or 0)
        reputation = float(identity.get("reputation") or 0)

        score = 10.0
        factors = [{"factor": "Base enterprise execution risk", "weight": 10}]

        if amount:
            amount_weight = min(35.0, amount / 200)
            score += amount_weight
            factors.append({"factor": f"Transaction amount {amount}", "weight": round(amount_weight, 2)})
        if trust_score < 75:
            score += 15
            factors.append({"factor": "Agent trust score below 75", "weight": 15})
        if reputation < 80:
            score += 12
            factors.append({"factor": "Agent reputation below 80", "weight": 12})
        if any(token in operation for token in ["delete", "refund", "payment", "payout"]):
            score += 14
            factors.append({"factor": f"Sensitive operation {operation}", "weight": 14})
        if service in {"Payment Service", "Refund Service", "Invoice Service"}:
            score += 8
            factors.append({"factor": f"Financial service {service}", "weight": 8})

        score = min(round(score, 2), 100.0)
        category = "LOW"
        if score >= 70:
            category = "HIGH"
        elif score >= 40:
            category = "MEDIUM"
        return {
            "score": score,
            "category": category,
            "factors": factors,
            "confidence": 0.91,
            "explanation": f"Risk is {category.lower()} with score {score}.",
        }
