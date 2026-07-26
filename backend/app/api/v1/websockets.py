from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.database.session import SessionLocal
from app.graph.graph import GovernanceGraph
from app.services.container import build_service_container


router = APIRouter(tags=["WebSockets"])


@router.websocket("/ws/governance/live")
async def live_governance(websocket: WebSocket) -> None:
    await websocket.accept()
    db = SessionLocal()
    try:
        services = build_service_container(db)

        async def emit(event: dict) -> None:
            await websocket.send_json({"type": "node_event", "event": event})

        while True:
            message = await websocket.receive_json()
            request = message.get("request", message)
            simulation = bool(message.get("simulation", False))
            graph = GovernanceGraph(services, emit)
            result = await graph.execute(request, simulation=simulation)
            await websocket.send_json({"type": "final", "response": result.get("response"), "state": result})
    except WebSocketDisconnect:
        return
    finally:
        db.close()
