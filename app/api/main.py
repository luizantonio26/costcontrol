


from fastapi import APIRouter

from app.api.routers import teste_router


api_router = APIRouter()

api_router.include_router(teste_router.router, tags=["hello world"])