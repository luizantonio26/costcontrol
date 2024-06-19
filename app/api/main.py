


from fastapi import APIRouter

from app.api.routers import recipe_router, teste_router, user_router


api_router = APIRouter()

api_router.include_router(user_router.router, tags=["user"])
api_router.include_router(recipe_router.router, tags=["recipe"])