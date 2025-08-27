from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.routes import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🐭 Incializando todo lo necesario...")
    yield
    print("🐭 Finalizando todo lo necesario...")

app = FastAPI(title="Yamaha Administrative API", lifespan=lifespan)

app.include_router(api_router)