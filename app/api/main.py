


from fastapi import APIRouter

from app.api.routers import teste_router, user_router


api_router = APIRouter()

api_router.include_router(user_router.router, tags=["user"])