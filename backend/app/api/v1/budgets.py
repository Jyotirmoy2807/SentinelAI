from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_services
from app.schemas.budget import BudgetProfileCreate, BudgetProfileRead, BudgetProfileUpdate
from app.services.container import ServiceContainer


router = APIRouter(prefix="/budget", tags=["Budget"])


@router.get("", response_model=list[BudgetProfileRead])
def list_profiles(services: ServiceContainer = Depends(get_services)):
    return services.budget.list_profiles()


@router.post("", response_model=BudgetProfileRead, status_code=status.HTTP_201_CREATED)
def create_profile(payload: BudgetProfileCreate, services: ServiceContainer = Depends(get_services)):
    return services.budget.create_profile(payload.model_dump())


@router.put("/{profile_id}", response_model=BudgetProfileRead)
def update_profile(profile_id: int, payload: BudgetProfileUpdate, services: ServiceContainer = Depends(get_services)):
    profile = services.budget.get_profile(profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Budget profile not found")
    return services.budget.update_profile(profile, payload.model_dump(exclude_unset=True))


@router.delete("/{profile_id}", response_model=BudgetProfileRead)
def delete_profile(profile_id: int, services: ServiceContainer = Depends(get_services)):
    profile = services.budget.get_profile(profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Budget profile not found")
    return services.budget.delete_profile(profile)
