from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, computed_field
from typing import List, Optional

from app.api.models import ingredients
from app.api.schemas.recipe_ingredients_schemas import RecipeIngredientResponse

class CreateRecipeRequest(BaseModel):
    name: str = Field(min_length=3, max_length=150)
    image_url: str | None = None
    prep_time: str = Field(min_length=2, max_length=10)
    servings: int = Field(gt=0)
    
class RecipeResponse(BaseModel):
    id: int 
    user_id: int
    name: str
    prep_time: str
    servings: int
    image_url: str | None = None
    ingredients: List[RecipeIngredientResponse]
    created_at: datetime
    updated_at: datetime
    
    @computed_field
    @property
    def recipe_cost(self) -> float:
        total_cost = 0
        for i in self.ingredients:
            total_cost += i.value
            
        return total_cost
    
    @computed_field
    @property
    def recipe_cost_per_unit(self) -> float:
            
        return self.recipe_cost / self.servings
    
    model_config = ConfigDict(from_attributes=True)


class PartialUpdateRecipeRequest(BaseModel):
    name: Optional[str] = None
    prep_time: Optional[str] = None
    servings: Optional[int] = None
    image_url: Optional[str] = None