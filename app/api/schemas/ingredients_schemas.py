from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class CreateIngredientRequest(BaseModel):
    name: str = Field(min_length=3, max_length=150)
    quantity: float = Field(gt=0)
    unit: str = Field(min_length=1)
    value: float = Field(gt=0)
    
class PartialIngredientRequest(BaseModel):
    name: Optional[str] = None
    quantity: Optional[str] = None
    unit: Optional[str] = None
    value: Optional[float] = None
    
class IngredientResponse(BaseModel):
    id: int 
    name: str
    quantity: float
    unit: str
    value: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)