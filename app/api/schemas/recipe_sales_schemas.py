from datetime import date
from pydantic import BaseModel, ConfigDict, Field, computed_field

from app.api.schemas.recipe_schemas import RecipeResponse

class CreateRecipeSalesRequest(BaseModel):
    client_name: str
    quantity: float = Field(gt=0)
    sale_date: date
    recipe_id: int

class UpdateRecipeSalesRequest(BaseModel):
    client_name: str
    quantity: float = Field(gt=0)
    sale_date: date
    
class RecipeSalesResponse(BaseModel):
    id: int 
    client_name: str
    quantity: float = Field(gt=0)
    sale_date: date
    recipe: RecipeResponse
    
    @computed_field
    @property
    def value(self) -> float:
        return self.quantity * (self.recipe.recipe_cost_per_unit + (self.recipe.recipe_cost_per_unit * 2.5))
    
    model_config = ConfigDict(
        from_attributes=True
    )