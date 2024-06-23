


from fastapi import APIRouter

from app.api.routers import ingredient_router, recipe_ingredients_router, recipe_router, recipe_sale_router, teste_router, user_router


api_router = APIRouter()

api_router.include_router(user_router.router, tags=["user"])
api_router.include_router(recipe_router.router, tags=["recipe"])
api_router.include_router(ingredient_router.router, tags=["ingredient"])
api_router.include_router(recipe_ingredients_router.router, tags=["recipe ingredients"])
api_router.include_router(recipe_sale_router.router, tags=["recipe sales"])