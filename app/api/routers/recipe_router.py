from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.api.models.recipes import Recipe
from app.api.models.user import User
from app.api.schemas.recipe_schemas import CreateRecipeRequest, PartialUpdateRecipeRequest, RecipeResponse
from app.configs.dependencies import get_db
from sqlalchemy.orm import Session
import base64
import uuid
import os

from app.configs.security import get_current_user

router = APIRouter(prefix="/recipe")

UPLOAD_DIR = "./app/api/media/images"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def image_upload(base64string: str):
    try:
        # Remove the header if it exists
        if base64string.startswith('data:image'):
            base64string = base64string.split(',')[1]
        # Decode the base64 string
        image_data = base64.b64decode(base64string)

        # Create a unique filename
        filename = f"{uuid.uuid4()}.png"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Save the image
        with open(file_path, "wb") as f:
            f.write(image_data)

        return {"filename": filename, "file_path": file_path}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")

class ImageBase64(BaseModel):
    base64_str: str

@router.get("/{recipe_id}/image/")
async def get_image(recipe_id:int, user: Annotated[User, Depends(get_current_user)], db:Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.user_id == user.id).first()
    
    if recipe is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "recipe not found")
    if recipe.image_url is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "recipe image not found")
    
    file_path = os.path.join(UPLOAD_DIR, recipe.image_url) # type: ignore
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='image/png')
    else:
        raise HTTPException(status_code=404, detail="Image not found")

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
    image:str | None = None
    if recipe_request.image_url:
        img = image_upload(recipe_request.image_url)
        if img:
            image = img["filename"] # type: ignore
        
    del recipe_request.image_url
    recipe: Recipe = Recipe(**recipe_request.model_dump())
    recipe.user_id = user.id # type: ignore
    
    if image:
        recipe.image_url = image # type: ignore
    
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    
    return recipe

@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_a_recipe(user: Annotated[User, Depends(get_current_user)], recipe_id:int, recipe_request: CreateRecipeRequest, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.user_id == user.id).first()
    
    if recipe is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "recipe not found")
    
    image:str | None = None
    if recipe_request.image_url:
        if recipe_request.image_url != recipe.image_url:
            img = image_upload(recipe_request.image_url)
            if img:
                image = img["filename"] # type: ignore
                
            file_path = os.path.join(UPLOAD_DIR, recipe_request.image_url)
            if os.path.exists(file_path):
                os.remove(file_path)
            recipe.image_url = image # type: ignore
    del recipe_request.image_url
    
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
    
    image:str | None = None
    if recipe_request.image_url:
        if recipe_request.image_url != recipe.image_url:
            img = image_upload(recipe_request.image_url)
            if img:
                image = img["filename"] # type: ignore
                
            file_path = os.path.join(UPLOAD_DIR, recipe_request.image_url)
            if os.path.exists(file_path):
                os.remove(file_path)
            recipe.image_url = image # type: ignore
    del recipe_request.image_url
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    
    return recipe