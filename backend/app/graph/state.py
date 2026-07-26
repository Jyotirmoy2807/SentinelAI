from collections.abc import Awaitable, Callable
from typing import Any, TypedDict


class GovernanceState(TypedDict, total=False):
    incoming_request: dict[str, Any]
    request: dict[str, Any]
    metadata: dict[str, Any]
    identity: dict[str, Any]
    normalized_execution: dict[str, Any]
    policy: dict[str, Any]
    risk: dict[str, Any]
    approval: dict[str, Any]
    audit: dict[str, Any]
    execution: dict[str, Any]
    explainability: dict[str, Any]
    response: dict[str, Any]
    events: list[dict[str, Any]]
    simulation: bool
    fatal_error: bool


EventSink = Callable[[dict[str, Any]], Awaitable[None]]
