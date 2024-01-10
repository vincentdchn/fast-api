from fastapi.routing import APIRouter

from pm_api.web.api import echo, monitoring, users

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(users.router, tags=["users"])
