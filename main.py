from contextlib import asynccontextmanager

from fastapi import FastAPI

from yamaha_bot_backend.api.routes import api_router
from yamaha_bot_backend.infrastructure.mqtt_async import mqtt
from yamaha_bot_backend.services.telemetry_store import telemetry_store


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("🐭 Incializando todo lo necesario...")
    # Cada mensaje recibido por MQTT será procesado por el store
    mqtt.add_message_handler(telemetry_store.ingest)
    # Conecta al broker
    await mqtt.connect()

    try:
        yield
    finally:
        print("🐭 Finalizando todo lo necesario...")
        # Desconecta al broker
        await mqtt.disconnect()


app = FastAPI(title="Yamaha Administrative API", lifespan=lifespan)
app.include_router(api_router)


# Endpoint de salud
@app.get("/")
def root():
    return {"msg": "Museum Robot API is running"}
