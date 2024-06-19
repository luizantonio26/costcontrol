from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.models.recipes import CreateRecipeRequest, PartialUpdateRecipeRequest, Recipe, RecipeResponse
from app.api.models.user import User
from app.configs.dependencies import get_db
from sqlalchemy.orm import Session

from app.configs.security import get_current_user

router = APIRouter(prefix="/recipe")


@router.get("/", response_model=List[RecipeResponse])
def list_recipes(user: Annotated[User, Depends(get_current_user)], db:Session = Depends(get_db))->List[RecipeResponse]:
    recipes = db.query(Recipe).filter(Recipe.user_id == user.id).all()
    return  recipes# type: ignore

@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(user: Annotated[User, Depends(get_current_user)], recipe_id:int, db: Session = Depends(get_db)) -> RecipeResponse:
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.user_id == User.id).first()
    if recipe is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "recipe not found")
    return recipe # type: ignore

@router.post("/", response_model=RecipeResponse)
def create_a_recipe(user: Annotated[User, Depends(get_current_user)], recipe_request: CreateRecipeRequest, db: Session = Depends(get_db)):
    recipe: Recipe = Recipe(**recipe_request.model_dump())
    recipe.user_id = user.id
    
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    
    return recipe

@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_a_recipe(user: Annotated[User, Depends(get_current_user)], recipe_id:int, recipe_request: CreateRecipeRequest, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.user_id == user.id).first()
    
    if recipe is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "recipe not found")
    
    recipe.name = recipe_request.name # type: ignore
    recipe.prep_time = recipe_request.prep_time # type: ignore
    recipe.servings = recipe_request.servings # type: ignore
    
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    
    return recipe

@router.patch("/{recipe_id}", response_model=RecipeResponse)
def partial_update_of_a_recipe(user: Annotated[User, Depends(get_current_user)], recipe_id:int, recipe_request: PartialUpdateRecipeRequest, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.user_id == user.id).first()
    
    if recipe is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "recipe not found")
    
    if not recipe_request.name and not recipe_request.prep_time and not recipe_request.servings:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "the body sent can't be empty")
    
    if recipe_request.name:
        recipe.name = recipe_request.name # type: ignore
    if recipe_request.prep_time:
        recipe.prep_time = recipe_request.prep_time # type: ignore
    if recipe_request.servings:
        recipe.servings = recipe_request.servings # type: ignore
    
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    
    return recipe