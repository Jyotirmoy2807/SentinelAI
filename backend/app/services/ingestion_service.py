from uuid import uuid4

from app.core.config import Settings
from app.utils.time import utc_iso_ms, utc_now


class IngestionService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def initialize_state(self, raw_request: dict, simulation: bool = False) -> dict:
        now = utc_now()
        timestamp = utc_iso_ms(now)
        request_id = f"REQ-{uuid4().hex[:12].upper()}"
        trace_id = f"TRC-{uuid4().hex[:12].upper()}"
        workflow_id = f"WFL-{uuid4().hex[:12].upper()}"
        return {
            "request": {
                "raw": raw_request,
                "timestamp": timestamp,
                "client_metadata": raw_request.get("metadata", {}),
            },
            "metadata": {
                "request_id": request_id,
                "trace_id": trace_id,
                "workflow_id": workflow_id,
                "graph_version": self.settings.graph_version,
                "timestamp": timestamp,
                "execution_duration_ms": 0,
            },
            "simulation": simulation,
        }
