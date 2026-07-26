package sentinelai.governance

default decision := {"decision": "ALLOW", "matched_policy": "default_allow", "reasons": ["No governance or budget policy matched."]}

decision := result if {
	policy := selected_policy
	result := {"decision": policy.decision, "matched_policy": policy.policy_id, "reasons": [policy.reason], "priority": policy.priority}
}

ranked_matches[key] := policy if {
	some policy in policy_matches
	key := sprintf("%06d:%s", [1000000 - policy.priority, policy.policy_id])
}

selected_policy := ranked_matches[keys[0]] if {
	count(ranked_matches) > 0
	keys := sort(object.keys(ranked_matches))
}

policy_matches contains policy if {
	input.identity.status != "ACTIVE"
	policy := {"decision": "DENY", "policy_id": "blocked_agent_deny", "priority": 990000, "reason": "Agent Passport is not active."}
}

policy_matches contains policy if {
	input.normalizedExecution.operation == "delete_database"
	policy := {"decision": "DENY", "policy_id": "destructive_action_deny", "priority": 980000, "reason": "Destructive database operations are forbidden."}
}

policy_matches contains policy if {
	input.risk.score >= 70
	policy := {"decision": "REQUIRE_APPROVAL", "policy_id": "high_risk_approval", "priority": 880000, "reason": "High NIST RMF risk score requires human approval."}
}

policy_matches contains policy if {
	input.identity.department == "Finance"
	input.normalizedExecution.amount >= 5000
	policy := {"decision": "REQUIRE_APPROVAL", "policy_id": "finance_amount_approval", "priority": 870000, "reason": "Finance transaction amount requires governance approval."}
}

policy_matches contains policy if {
	input.identity.department == "Finance"
	amount := input.normalizedExecution.amount
	amount > 10000
	policy := {"decision": "DENY", "policy_id": "budget_finance_controlled_transaction_limit", "priority": 900000, "reason": "Finance-Controlled transaction limit exceeded."}
}

policy_matches contains policy if {
	input.identity.department == "Finance"
	amount := input.normalizedExecution.amount
	amount + 0 > 25000
	policy := {"decision": "DENY", "policy_id": "budget_finance_controlled_daily_limit", "priority": 899999, "reason": "Finance-Controlled daily limit exceeded."}
}

policy_matches contains policy if {
	input.identity.department == "Finance"
	amount := input.normalizedExecution.amount
	amount + 0 > 250000
	policy := {"decision": "DENY", "policy_id": "budget_finance_controlled_monthly_limit", "priority": 899998, "reason": "Finance-Controlled monthly limit exceeded."}
}

policy_matches contains policy if {
	input.identity.department == "Finance"
	amount := input.normalizedExecution.amount
	amount >= 5000
	policy := {"decision": "REQUIRE_APPROVAL", "policy_id": "budget_finance_controlled_approval_threshold", "priority": 899997, "reason": "Finance-Controlled approval threshold reached."}
}

policy_matches contains policy if {
	input.identity.department == "HR"
	amount := input.normalizedExecution.amount
	amount > 3000
	policy := {"decision": "DENY", "policy_id": "budget_hr_travel_transaction_limit", "priority": 899990, "reason": "HR-Travel transaction limit exceeded."}
}

policy_matches contains policy if {
	input.identity.department == "HR"
	amount := input.normalizedExecution.amount
	amount + 0 > 8000
	policy := {"decision": "DENY", "policy_id": "budget_hr_travel_daily_limit", "priority": 899989, "reason": "HR-Travel daily limit exceeded."}
}

policy_matches contains policy if {
	input.identity.department == "HR"
	amount := input.normalizedExecution.amount
	amount + 0 > 60000
	policy := {"decision": "DENY", "policy_id": "budget_hr_travel_monthly_limit", "priority": 899988, "reason": "HR-Travel monthly limit exceeded."}
}

policy_matches contains policy if {
	input.identity.department == "HR"
	amount := input.normalizedExecution.amount
	amount >= 1000
	policy := {"decision": "REQUIRE_APPROVAL", "policy_id": "budget_hr_travel_approval_threshold", "priority": 899987, "reason": "HR-Travel approval threshold reached."}
}

policy_matches contains policy if {
	input.identity.department == "IT"
	amount := input.normalizedExecution.amount
	amount > 1000
	policy := {"decision": "DENY", "policy_id": "budget_it_restricted_transaction_limit", "priority": 899970, "reason": "IT-Restricted transaction limit exceeded."}
}

policy_matches contains policy if {
	input.identity.department == "IT"
	amount := input.normalizedExecution.amount
	amount + 0 > 2500
	policy := {"decision": "DENY", "policy_id": "budget_it_restricted_daily_limit", "priority": 899969, "reason": "IT-Restricted daily limit exceeded."}
}

policy_matches contains policy if {
	input.identity.department == "IT"
	amount := input.normalizedExecution.amount
	amount + 0 > 20000
	policy := {"decision": "DENY", "policy_id": "budget_it_restricted_monthly_limit", "priority": 899968, "reason": "IT-Restricted monthly limit exceeded."}
}

policy_matches contains policy if {
	input.identity.department == "IT"
	amount := input.normalizedExecution.amount
	amount >= 500
	policy := {"decision": "REQUIRE_APPROVAL", "policy_id": "budget_it_restricted_approval_threshold", "priority": 899967, "reason": "IT-Restricted approval threshold reached."}
}

policy_matches contains policy if {
	input.identity.department == "Operations"
	amount := input.normalizedExecution.amount
	amount > 4000
	policy := {"decision": "DENY", "policy_id": "budget_operations_standard_transaction_limit", "priority": 899980, "reason": "Operations-Standard transaction limit exceeded."}
}

policy_matches contains policy if {
	input.identity.department == "Operations"
	amount := input.normalizedExecution.amount
	amount + 0 > 12000
	policy := {"decision": "DENY", "policy_id": "budget_operations_standard_daily_limit", "priority": 899979, "reason": "Operations-Standard daily limit exceeded."}
}

policy_matches contains policy if {
	input.identity.department == "Operations"
	amount := input.normalizedExecution.amount
	amount + 0 > 100000
	policy := {"decision": "DENY", "policy_id": "budget_operations_standard_monthly_limit", "priority": 899978, "reason": "Operations-Standard monthly limit exceeded."}
}

policy_matches contains policy if {
	input.identity.department == "Operations"
	amount := input.normalizedExecution.amount
	amount >= 1500
	policy := {"decision": "REQUIRE_APPROVAL", "policy_id": "budget_operations_standard_approval_threshold", "priority": 899977, "reason": "Operations-Standard approval threshold reached."}
}

policy_matches contains policy if {
	input.identity.department == "Sales"
	amount := input.normalizedExecution.amount
	amount > 5000
	policy := {"decision": "DENY", "policy_id": "budget_sales_refunds_transaction_limit", "priority": 899990, "reason": "Sales-Refunds transaction limit exceeded."}
}

policy_matches contains policy if {
	input.identity.department == "Sales"
	amount := input.normalizedExecution.amount
	amount + 0 > 15000
	policy := {"decision": "DENY", "policy_id": "budget_sales_refunds_daily_limit", "priority": 899989, "reason": "Sales-Refunds daily limit exceeded."}
}

policy_matches contains policy if {
	input.identity.department == "Sales"
	amount := input.normalizedExecution.amount
	amount + 0 > 150000
	policy := {"decision": "DENY", "policy_id": "budget_sales_refunds_monthly_limit", "priority": 899988, "reason": "Sales-Refunds monthly limit exceeded."}
}

policy_matches contains policy if {
	input.identity.department == "Sales"
	amount := input.normalizedExecution.amount
	amount >= 750
	policy := {"decision": "REQUIRE_APPROVAL", "policy_id": "budget_sales_refunds_approval_threshold", "priority": 899987, "reason": "Sales-Refunds approval threshold reached."}
}
