from datetime import date
from typing import List
from pydantic import BaseModel, ConfigDict, Field, computed_field

from app.api.schemas.recipe_schemas import RecipeResponse
from app.api.schemas.sales_item_schemas import SaleItemsRequest, SaleItemsResponse

class CreateRecipeSalesRequest(BaseModel):
    client_name: str
    payment_method: str
    payment_status: str
    sale_date: date
    items: List[SaleItemsRequest]

class UpdateRecipeSalesRequest(BaseModel):
    client_name: str
    payment_method: str
    payment_status: str
    sale_date: date
    
class RecipeSalesResponse(BaseModel):
    id: int
    client_name: str
    payment_method: str | None = None
    payment_status: str | None = None
    sale_date: date
    items: List[SaleItemsResponse]
    
    @computed_field
    @property
    def total_value(self) -> float:
        total = 0
        for i in self.items:
            total += i.value
        return total
    
    model_config = ConfigDict(
        from_attributes=True
    )