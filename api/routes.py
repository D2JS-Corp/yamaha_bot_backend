from fastapi import APIRouter

api_router = APIRouter()

@api_router.get("/")
def root():
    return {"msg": "Museum Robot API is running"}