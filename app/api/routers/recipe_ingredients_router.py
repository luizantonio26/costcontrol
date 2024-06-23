

from typing import Annotated, List
from fastapi import APIRouter, status, Depends, HTTPException

from app.api.models.recipe_ingredients import RecipeIngredients
from app.api.models.user import User
from app.api.models.ingredients import Ingredients
from app.api.models.recipes import Recipe
from app.api.schemas.recipe_ingredients_schemas import CreateRecipeIngredientRequest, RecipeIngredientResponse, UpdateRecipeIngredientRequest
from app.configs.dependencies import get_db
from app.configs.security import get_current_user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/recipe_ingredients")

@router.post("/", response_model=RecipeIngredientResponse)
def add_ingredient_to_a_recipe(ingredient_recipe_request:CreateRecipeIngredientRequest, user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)) -> RecipeIngredientResponse:
    recipe = db.query(Recipe).filter(Recipe.id == ingredient_recipe_request.recipe_id, Recipe.user_id == user.id).first()
    
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    
    ingredient = db.query(Ingredients).filter(Ingredients.id == ingredient_recipe_request.ingredient_id).first()
    
    if not ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
    
    recipe_ingredient = RecipeIngredients(
        quantity = ingredient_recipe_request.quantity,
        recipe_id = recipe.id,
        ingredient_id=ingredient.id
    )

    db.add(recipe_ingredient)
    db.commit()
    db.refresh(recipe_ingredient)
    
    
    return recipe_ingredient # type: ignore


@router.get("/{recipe_id}", response_model=List[RecipeIngredientResponse])
def list_ingredient_of_a_recipe(recipe_id: int, user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)) -> List[RecipeIngredientResponse]:
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.user_id == user.id).first()
    
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    
    recipe_ingredients = db.query(RecipeIngredients).filter(RecipeIngredients.recipe_id == recipe_id)
    
    return recipe_ingredients # type: ignore

@router.put("/{recipe_ingredient_id}", response_model=RecipeIngredientResponse)
def update_ingredient_of_a_recipe(recipe_ingredient_id: int, ingredient_recipe_request:UpdateRecipeIngredientRequest, user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)) -> RecipeIngredientResponse:
    recipe = db.query(Recipe).filter(Recipe.id == ingredient_recipe_request.recipe_id, Recipe.user_id == user.id).first()
    
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    
    recipe_ingredient: RecipeIngredients = db.query(RecipeIngredients).get(recipe_ingredient_id) # type: ignore

    recipe_ingredient.quantity = ingredient_recipe_request.quantity # type: ignore
    
    db.add(recipe_ingredient)
    db.commit()
    db.refresh(recipe_ingredient)
    
    
    return recipe_ingredient # type: ignore