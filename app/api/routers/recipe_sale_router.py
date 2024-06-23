


from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.api.models.recipe_sales import RecipeSales
from app.api.models.recipes import Recipe
from app.api.models.user import User
from app.api.schemas.recipe_sales_schemas import CreateRecipeSalesRequest, RecipeSalesResponse
from app.configs.dependencies import get_db
from app.configs.security import get_current_user



router = APIRouter(prefix="/sales")


@router.get("/", response_model=List[RecipeSalesResponse])
def list_sales(user: Annotated[User, Depends(get_current_user)], db: Session=Depends(get_db))->List[RecipeSalesResponse]:
    sales = db.query(RecipeSales).join(Recipe).filter(Recipe.user_id == user.id).all()
    
    response: List[RecipeSalesResponse] = [
        RecipeSalesResponse.from_orm(sale) for sale in sales
    ]
    
    return response


@router.post("/", response_model=RecipeSalesResponse)
def create_sales(sale_request: CreateRecipeSalesRequest, user: Annotated[User, Depends(get_current_user)], db: Session=Depends(get_db))->RecipeSalesResponse:
    recipe = db.query(Recipe).filter(Recipe.id == sale_request.recipe_id, Recipe.user_id == user.id).first()
    
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    
    recipe_sale = RecipeSales(**sale_request.model_dump())
    
    db.add(recipe_sale)
    db.commit()
    db.refresh(recipe_sale)
    
    return recipe_sale # type: ignore