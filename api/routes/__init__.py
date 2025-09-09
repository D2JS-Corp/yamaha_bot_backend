from fastapi import APIRouter

from yamaha_bot_backend.core.config import settings

from .robot import router as robot_router

api_router = APIRouter(prefix=settings.API_V1_PREFIX)
api_router.include_router(robot_router)
