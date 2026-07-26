from collections.abc import Awaitable, Callable
from datetime import datetime
from time import perf_counter
from typing import Any
from uuid import uuid4

from app.graph.state import GovernanceState


NodeAction = Callable[[GovernanceState], Awaitable[dict[str, Any]]]
StatusResolver = Callable[[GovernanceState], str]


async def run_governance_node(
    state: GovernanceState,
    node_name: str,
    action: NodeAction,
    event_sink: Callable[[dict[str, Any]], Awaitable[None]] | None = None,
    status_resolver: StatusResolver | None = None,
) -> dict[str, Any]:
    started = perf_counter()
    existing_events = list(state.get("events", []))
    start_event = _event(state, node_name, "RUNNING", 0, {})
    existing_events.append(start_event)
    await _emit(event_sink, start_event)

    try:
        updates = await action(state)
        merged_state = {**state, **updates}
        duration_ms = round((perf_counter() - started) * 1000, 2)
        completed_status = status_resolver(merged_state) if status_resolver else "COMPLETED"
        completed_event = _event(merged_state, node_name, completed_status, duration_ms, _event_payload(node_name, merged_state))
        existing_events.append(completed_event)
        await _emit(event_sink, completed_event)
        updates["events"] = existing_events
        return updates
    except Exception as exc:
        duration_ms = round((perf_counter() - started) * 1000, 2)
        failed_event = _event(state, node_name, "FAILED", duration_ms, {"error": str(exc)})
        existing_events.append(failed_event)
        await _emit(event_sink, failed_event)
        return {
            "fatal_error": True,
            "events": existing_events,
            "audit": {
                "decision": "ERROR",
                "status": "FAILED",
                "error": str(exc),
            },
            "explainability": {
                "summary": "ERROR",
                "narrative": f"{node_name} failed: {exc}",
                "sections": [],
            },
            "response": {
                "metadata": state.get("metadata", {}),
                "governance": {
                    "decision": "ERROR",
                    "reasons": [str(exc)],
                    "approval_status": state.get("approval", {}).get("status", "NOT_REQUIRED"),
                },
                "result": None,
                "explainability": {},
                "state": state,
            },
        }


def status_from_decision(section: str) -> StatusResolver:
    def resolver(state: GovernanceState) -> str:
        payload = state.get(section, {})
        decision = payload.get("decision") or payload.get("status")
        if decision in {"DENY", "REJECTED"}:
            return "DENIED"
        if decision in {"REQUIRE_APPROVAL", "PENDING"}:
            return "WAITING_APPROVAL" if section == "approval" else "COMPLETED"
        if decision in {"ERROR", "FAILED"}:
            return "FAILED"
        return "COMPLETED"

    return resolver


def _event(state: GovernanceState, node_name: str, status: str, duration_ms: float, payload: dict[str, Any]) -> dict[str, Any]:
    request_id = state.get("metadata", {}).get("request_id", "UNASSIGNED")
    normalized = state.get("normalized_execution", {})
    identity = state.get("identity", {})
    policy = state.get("policy", {})
    risk = state.get("risk", {})
    approval = state.get("approval", {})
    decision = payload.get("decision") or policy.get("decision") or identity.get("decision") or status
    reason = _reason_from_payload(payload)
    return {
        "eventId": f"EVT-{uuid4().hex[:12].upper()}",
        "request_id": request_id,
        "requestId": request_id,
        "node": node_name,
        "stage": node_name,
        "status": status,
        "timestamp": datetime.utcnow().isoformat(),
        "duration_ms": duration_ms,
        "latency": duration_ms,
        "agent": identity.get("agent_name") or identity.get("passport_id") or normalized.get("passport_id", ""),
        "action": normalized.get("operation", ""),
        "policy": policy.get("matched_policy", ""),
        "riskScore": risk.get("score", 0),
        "decision": decision,
        "approvalStatus": approval.get("status", "NOT_REQUIRED"),
        "reason": reason,
        "enterpriseAPI": normalized.get("service", ""),
        "payload": payload,
    }


def _event_payload(node_name: str, state: GovernanceState) -> dict[str, Any]:
    section = {
        "api_ingestion": "metadata",
        "request_normalization": "normalized_execution",
        "agent_identity": "identity",
        "policy_engine": "policy",
        "risk_engine": "risk",
        "human_approval": "approval",
        "audit_engine": "audit",
        "enterprise_execution": "execution",
        "explainability": "explainability",
        "response_builder": "response",
    }.get(node_name)
    return state.get(section, {}) if section else {}


def _reason_from_payload(payload: dict[str, Any]) -> str:
    if payload.get("reason"):
        return str(payload["reason"])
    reasons = payload.get("reasons")
    if isinstance(reasons, list) and reasons:
        return str(reasons[0])
    if payload.get("explanation"):
        return str(payload["explanation"])
    if payload.get("status"):
        return str(payload["status"])
    return ""


async def _emit(event_sink: Callable[[dict[str, Any]], Awaitable[None]] | None, event: dict[str, Any]) -> None:
    if event_sink:
        await event_sink(event)
