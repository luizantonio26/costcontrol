


from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.api.models.recipe_sales import RecipeSales
from app.api.models.recipe_sales_item import RecipeSalesItem
from app.api.models.recipes import Recipe
from app.api.models.user import User
from app.api.schemas.recipe_sales_schemas import CreateRecipeSalesRequest, RecipeSalesResponse, UpdateRecipeSalesRequest
from app.configs.dependencies import get_db
from app.configs.security import get_current_user



router = APIRouter(prefix="/sales")


@router.get("/", response_model=List[RecipeSalesResponse])
def list_sales(user: Annotated[User, Depends(get_current_user)], db: Session=Depends(get_db))->List[RecipeSalesResponse]:
    sales = db.query(RecipeSales).filter(RecipeSales.user_id == user.id)
    
    
    # sales = db.query(RecipeSales).join(Recipe).filter(Recipe.user_id == user.id).all()
    
    # response: List[RecipeSalesResponse] = [
    #     RecipeSalesResponse.from_orm(sale) for sale in sales
    # ]
    
    return sales


@router.post("/", response_model=RecipeSalesResponse)
def create_sales(sale_request: CreateRecipeSalesRequest, user: Annotated[User, Depends(get_current_user)], db: Session=Depends(get_db))->RecipeSalesResponse:    
    items = sale_request.items
    del sale_request.items
    
    recipe_sale = RecipeSales(**sale_request.model_dump())
    recipe_sale.user_id = user.id # type: ignore
    
    db.add(recipe_sale)
    db.commit()
    db.refresh(recipe_sale)
    
    recipe_errors = []
    
    if len(items) != 0:
        for item in items:
            recipe = db.query(Recipe).where(Recipe.id == item.recipe_id, Recipe.user_id == user.id).first()
            
            if recipe:
                recipe_sale_item = RecipeSalesItem(**item.model_dump())
                recipe_sale_item.recipe_sales_id = recipe_sale.id
                db.add(recipe_sale_item)
                db.commit()
                db.refresh(recipe_sale_item)
            else:
                recipe_errors.append(item)
    
        if len(recipe_errors) == len(items):
            db.delete(recipe_sale)
            db.commit()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipes not found")
        
    db.refresh(recipe_sale)
    
    return recipe_sale
    

@router.put("/{sale_id}", response_model=RecipeSalesResponse)
def update_sales(sale_id: int, sale_request: UpdateRecipeSalesRequest, user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db))->RecipeSalesResponse:
    recipe_sale = db.query(RecipeSales).filter(RecipeSales.id == sale_id, RecipeSales.user_id == user.id).first()
    
    if not recipe_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe sale not found")
    
    recipe_sale.client_name = sale_request.client_name # type: ignore
    recipe_sale.sale_date = sale_request.sale_date # type: ignore
    recipe_sale.payment_method = sale_request.payment_method # type: ignore
    recipe_sale.payment_status = sale_request.payment_status # type: ignore
    
    db.add(recipe_sale)
    db.commit()
    db.refresh(recipe_sale)
    
    return recipe_sale # type: ignore

@router.get("/{sale_id}", response_model=RecipeSalesResponse)
def get_sale(sale_id: int, user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)) -> RecipeSalesResponse:
    recipe_sale = db.query(RecipeSales).filter(RecipeSales.id == sale_id, RecipeSales.user_id == user.id).first()
    
    if not recipe_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe sale not found")
    
    return recipe_sale # type: ignore

@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(sale_id: int, user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    recipe_sale = db.query(RecipeSales).filter(RecipeSales.id == sale_id, RecipeSales.user_id == user.id).first()
    
    if not recipe_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe sale not found")
    
    db.delete(recipe_sale)
    db.commit()