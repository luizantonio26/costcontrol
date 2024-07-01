from pydantic import BaseModel, ConfigDict, computed_field

from app.api.schemas.recipe_schemas import RecipeResponse



class SaleItemsRequest(BaseModel):
    recipe_id: int
    quantity: int
    
class SaleItemsResponse(BaseModel):
    recipe: RecipeResponse
    id: int
    quantity: int

    @computed_field
    @property
    def value(self) -> float:
        return self.quantity * (self.recipe.recipe_cost_per_unit + (self.recipe.recipe_cost_per_unit * 2.5))

    model_config = ConfigDict(
        from_attributes=True
    )