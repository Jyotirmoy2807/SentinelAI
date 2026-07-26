package sentinelai.governance

deny_reasons := [reason | deny_reason[reason]]
approval_reasons := [reason | approval_reason[reason]]

budget_limits := {
    "Finance-Controlled": {
        "transaction_limit": 10000,
        "approval_threshold": 2000,
    },
    "Sales-Refunds": {
        "transaction_limit": 5000,
        "approval_threshold": 500,
    },
    "Operations-Standard": {
        "transaction_limit": 2500,
        "approval_threshold": 1200,
    },
    "IT-Restricted": {
        "transaction_limit": 800,
        "approval_threshold": 300,
    },
}

allowed_service if {
    input.identity.allowedApis[_] == input.normalizedExecution.service
}

allowed_operation if {
    input.identity.allowedOperations[_] == input.normalizedExecution.operation
}

deny_reason contains reason if {
    input.identity.status != "ACTIVE"
    reason := "Agent Passport is not active."
}

deny_reason contains reason if {
    not allowed_service
    reason := sprintf(
        "%s is not allowed for this Agent Passport.",
        [input.normalizedExecution.service],
    )
}

deny_reason contains reason if {
    not allowed_operation
    reason := sprintf(
        "%s is not allowed for this Agent Passport.",
        [input.normalizedExecution.operation],
    )
}

deny_reason contains reason if {
    input.normalizedExecution.operation == "delete_database"
    reason := "Destructive database operations are forbidden by OPA policy."
}

deny_reason contains reason if {
    contains(
        lower(input.normalizedExecution.parameterText),
        "bypass approval",
    )
    reason := "Governance bypass instructions are forbidden by OPA policy."
}

deny_reason contains reason if {
    input.normalizedExecution.service == "Payroll Service"
    reason := "Payroll Service is restricted for autonomous agents."
}

deny_reason contains reason if {
    input.normalizedExecution.amount >
        budget_limits[input.identity.budgetProfile].transaction_limit

    reason := sprintf(
        "Amount %.2f exceeds transaction limit.",
        [input.normalizedExecution.amount],
    )
}

deny_reason contains reason if {
    input.normalizedExecution.operation == "export_personal_data"
    reason := "GDPR personal data export requires a dedicated governed workflow."
}

approval_reason contains reason if {
    count(deny_reasons) == 0

    input.normalizedExecution.amount >=
        budget_limits[input.identity.budgetProfile].approval_threshold

    input.normalizedExecution.amount > 0

    reason := "Transaction amount exceeds OPA approval threshold."
}

approval_reason contains reason if {
    count(deny_reasons) == 0
    input.risk.score >= 70
    reason := "NIST RMF risk score requires authorization review."
}

approval_reason contains reason if {
    count(deny_reasons) == 0
    input.normalizedExecution.service == "Payment Service"
    input.normalizedExecution.amount > 2000
    reason := "PCI DSS payment review is required for high-value payments."
}

decision := {
    "decision": "DENY",
    "matched_policy": "sentinelai/governance/deny",
    "reasons": deny_reasons,
} if {
    count(deny_reasons) > 0
}

decision := {
    "decision": "REQUIRE_APPROVAL",
    "matched_policy": "sentinelai/governance/approval",
    "reasons": approval_reasons,
} if {
    count(deny_reasons) == 0
    count(approval_reasons) > 0
}

decision := {
    "decision": "ALLOW",
    "matched_policy": "sentinelai/governance/allow",
    "reasons": [
        "OPA policy allowed governed enterprise execution.",
    ],
} if {
    count(deny_reasons) == 0
    count(approval_reasons) == 0
}