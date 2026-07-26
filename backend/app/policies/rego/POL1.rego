package sentinelai.custom

default decision := {
  "decision": "ALLOW",
  "matched_policy": "sentinelai.custom/default_allow",
  "reasons": ["Custom policy evaluated"],
}

decision := {
  "decision": "REQUIRE_APPROVAL",
  "matched_policy": "sentinelai.custom/high_risk_approval",
  "reasons": ["High risk requests require human approval"],
} if {
  input.risk.score >= 70
}
