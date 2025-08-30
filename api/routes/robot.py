from fastapi import APIRouter, HTTPException
from services.telemetry_store import telemetry_store

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