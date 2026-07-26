from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_services
from app.schemas.enterprise import EnterpriseAPICreate, EnterpriseAPIRead, EnterpriseAPIUpdate
from app.services.container import ServiceContainer


router = APIRouter(prefix="/enterprise", tags=["Enterprise API Registry"])


@router.get("", response_model=list[EnterpriseAPIRead])
def list_apis(services: ServiceContainer = Depends(get_services)):
    return services.enterprise_registry.list_apis()


@router.post("", response_model=EnterpriseAPIRead, status_code=status.HTTP_201_CREATED)
def create_api(payload: EnterpriseAPICreate, services: ServiceContainer = Depends(get_services)):
    try:
        return services.enterprise_registry.register_api(payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/lookups")
def lookups(services: ServiceContainer = Depends(get_services)):
    return services.enterprise_registry.lookups()


@router.get("/{api_id}", response_model=EnterpriseAPIRead)
def get_api(api_id: int, services: ServiceContainer = Depends(get_services)):
    api = services.enterprise_registry.get_api(api_id)
    if api is None:
        raise HTTPException(status_code=404, detail="Enterprise API not found")
    return api


@router.put("/{api_id}", response_model=EnterpriseAPIRead)
def update_api(api_id: int, payload: EnterpriseAPIUpdate, services: ServiceContainer = Depends(get_services)):
    api = services.enterprise_registry.get_api(api_id)
    if api is None:
        raise HTTPException(status_code=404, detail="Enterprise API not found")
    try:
        return services.enterprise_registry.update_api(api, payload.model_dump(exclude_unset=True))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{api_id}/activate", response_model=EnterpriseAPIRead)
def activate_api(api_id: int, services: ServiceContainer = Depends(get_services)):
    return _set_api_status(api_id, "ACTIVE", services)


@router.post("/{api_id}/deactivate", response_model=EnterpriseAPIRead)
def deactivate_api(api_id: int, services: ServiceContainer = Depends(get_services)):
    return _set_api_status(api_id, "INACTIVE", services)


@router.delete("/{api_id}", response_model=EnterpriseAPIRead)
def delete_api(api_id: int, services: ServiceContainer = Depends(get_services)):
    api = services.enterprise_registry.get_api(api_id)
    if api is None:
        raise HTTPException(status_code=404, detail="Enterprise API not found")
    return services.enterprise_registry.delete_api(api)


def _set_api_status(api_id: int, status_value: str, services: ServiceContainer):
    api = services.enterprise_registry.get_api(api_id)
    if api is None:
        raise HTTPException(status_code=404, detail="Enterprise API not found")
    return services.enterprise_registry.set_status(api, status_value)
