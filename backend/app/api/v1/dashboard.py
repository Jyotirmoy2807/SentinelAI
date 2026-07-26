from fastapi import APIRouter, Depends

from app.core.dependencies import get_services
from app.schemas.dashboard import DashboardResponse
from app.services.container import ServiceContainer


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(services: ServiceContainer = Depends(get_services)) -> dict:
    return services.dashboard.summary()
