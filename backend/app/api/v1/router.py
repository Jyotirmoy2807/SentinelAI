from fastapi import APIRouter

from app.api.v1 import agents, approvals, audit, budgets, compliance, dashboard, enterprise, firewall, governance, health, policies, settings, websockets


api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(dashboard.router)
api_router.include_router(agents.router)
api_router.include_router(policies.router)
api_router.include_router(firewall.router)
api_router.include_router(budgets.router)
api_router.include_router(compliance.router)
api_router.include_router(enterprise.router)
api_router.include_router(governance.router)
api_router.include_router(approvals.router)
api_router.include_router(audit.router)
api_router.include_router(settings.router)
api_router.include_router(websockets.router)
