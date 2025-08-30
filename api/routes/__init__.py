from fastapi import APIRouter
from .robot import router as robot_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(robot_router)