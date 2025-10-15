from fastapi import APIRouter, HTTPException

from yamaha_bot_backend.services.telemetry_store import telemetry_store
from yamaha_bot_backend.services.robot_service import robot_service

router = APIRouter(prefix="/robot", tags=["Robot"])


@router.get("/latest")
async def get_latest():
    return await telemetry_store.latest_all()


@router.get("/latest/{topic:path}")
async def get_latest_topic(topic: str):
    data = await telemetry_store.latest_by_topic(topic)
    if not data:
        raise HTTPException(status_code=404, detail="Tópico sin datos")
    return data


@router.get("/topic/{topic:path}")
async def get_topic_records(topic: str):
    """Obtiene los últimos registros de un tópico (máximo 12)"""
    records = await telemetry_store.topic(topic)
    return {
        "topic": topic,
        "count": len(records), #type: ignore
        "records": records
    }

@router.get("/position")
async def get_robot_position():
    return await robot_service.get_current_position()


@router.post("/move")
async def move_robot():
    result = await robot_service.move_to_next_base()
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
