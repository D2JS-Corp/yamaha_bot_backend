from contextlib import asynccontextmanager
import logging.config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from yamaha_bot_backend.api.routes import api_router
from yamaha_bot_backend.infrastructure.mqtt_async import mqtt
from yamaha_bot_backend.services.telemetry_store import telemetry_store
from yamaha_bot_backend.services.logger_service import main_logger
from yamaha_bot_backend.middleware.logging_middleware import LoggingMiddleware
from yamaha_bot_backend.core.logging_config import LOGGING_CONFIG


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Configurar logging
    logging.config.dictConfig(LOGGING_CONFIG)
    main_logger.info("🐭 Inicializando aplicación...")
    
    # Configurar MQTT
    mqtt.add_message_handler(telemetry_store.ingest)
    await mqtt.connect()
    main_logger.info("✅ MQTT configurado y conectado")

    try:
        main_logger.info("🚀 Aplicación iniciada correctamente")
        yield
    except Exception as e:
        main_logger.error("❌ Error durante la inicialización", exc_info=True)
        raise
    finally:
        print("🐭 Finalizando todo lo necesario...http://127.0.0.1:8000/api/v1/robot/topic/ros2%2Fbattery")
        # Desconecta al brokerhttp://127.0.0.1:8000/api/v1/robot/topic/ros2%2Fbattery
        await mqtt.disconnect()
        main_logger.info("✅ Aplicación finalizada correctamente")


app = FastAPI(title="Yamaha Administrative API", lifespan=lifespan)

# Agregar middleware de logging
app.add_middleware(LoggingMiddleware)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint de salud
@app.get("/")
def root():
    main_logger.info("Health check solicitado")
    return {"msg": "Museum Robot API is running"}