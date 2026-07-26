from fastapi import APIRouter, Depends

from app.core.dependencies import get_services
from app.schemas.settings import SettingsRead
from app.services.container import ServiceContainer


router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get("", response_model=SettingsRead)
def read_settings(services: ServiceContainer = Depends(get_services)):
    return services.settings_service.read()
