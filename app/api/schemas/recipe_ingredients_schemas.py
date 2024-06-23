from pydantic import BaseModel, ConfigDict, Field, computed_field

from app.api.schemas.ingredients_schemas import IngredientResponse

class CreateRecipeIngredientRequest(BaseModel):
    quantity: float = Field(gt=0)
    recipe_id: int
    ingredient_id: int

class UpdateRecipeIngredientRequest(BaseModel):
    quantity: float = Field(gt=0)
    recipe_id: int
    
class RecipeIngredientResponse(BaseModel):
    id: int 
    quantity: float
    ingredients: IngredientResponse
    
    @computed_field
    @property
    def value(self) -> float:
        
        
        return (self.quantity * self.ingredients.value) / self.ingredients.quantity
    
    model_config = ConfigDict(
        from_attributes=True
    )
    
class RecipeIngredientRecipeResponse(BaseModel):
    id: int 
    quantity: float
    ingredients: IngredientResponse
    
    @computed_field
    @property
    def value(self) -> float:
        return self.quantity * self.ingredients.value
    
    model_config = ConfigDict(
        from_attributes=True
    )