

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.models.ingredients import CreateIngredientRequest, IngredientResponse, Ingredients, PartialIngredientRequest
from app.configs.dependencies import get_db


router = APIRouter(prefix="/ingredient")


@router.get("/", response_model=List[IngredientResponse])
def list_ingredients(db: Session = Depends(get_db)) -> List[IngredientResponse]:
    return db.query(Ingredients).all() # type: ignore

@router.get("/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient_by_id(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = db.query(Ingredients).get(ingredient_id)
    
    if ingredient:
        return ingredient
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ingredient not found")


@router.post("/", response_model=IngredientResponse)
def create_ingredient(ingredient_request: CreateIngredientRequest, db: Session=Depends(get_db))->IngredientResponse:
    ingredient: Ingredients = Ingredients(**ingredient_request.model_dump())
    
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    
    return ingredient # type: ignore

@router.put("/{ingredient_id}", response_model=IngredientResponse)
def update_an_ingredient(ingredient_id:int, ingredient_request: CreateIngredientRequest, db: Session = Depends(get_db)):
    ingredient = db.query(Ingredients).filter(Ingredients.id == ingredient_id).first()
    
    if ingredient is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "ingredient not found")
    
    ingredient.name = ingredient_request.name # type: ignore
    ingredient.quantity = ingredient_request.quantity # type: ignore
    ingredient.value = ingredient_request.value # type: ignore
    ingredient.unit = ingredient_request.unit # type: ignore
    
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    
    return ingredient

@router.patch("/{ingredient_id}", response_model=IngredientResponse)
def partial_update_of_an_ingredient(ingredient_id:int, ingredient_request: PartialIngredientRequest, db: Session = Depends(get_db)):
    ingredient = db.query(Ingredients).filter(Ingredients.id == ingredient_id).first()
    
    if ingredient is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "ingredient not found")
    
    if not ingredient_request.name and not ingredient_request.quantity and not ingredient_request.unit and not ingredient_request.value:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "The body sent can't be empty")
    
    if ingredient_request.name:
        ingredient.name = ingredient_request.name # type: ignore
    if ingredient_request.quantity:
        ingredient.quantity = ingredient_request.quantity # type: ignore
    if ingredient_request.value:
        ingredient.value = ingredient_request.value # type: ignore
    if ingredient_request.unit:
        ingredient.unit = ingredient_request.unit # type: ignore
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    
    return ingredient