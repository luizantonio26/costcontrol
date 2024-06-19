from dataclasses import field
from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy import DECIMAL, Float, ForeignKey, Integer, func
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from api.models.ingredients import IngredientResponse, Ingredients
from api.models.recipes import Recipe

#from configs.database import Base

class Base(DeclarativeBase):
    pass

class RecipeIngredients(Base):
    __tablename__="recipe_ingredient"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quantity: Mapped[float] = mapped_column(Float)
    recipe_id: Mapped[int] = mapped_column(ForeignKey(Recipe.id))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey(Ingredients.id))
    parent: Mapped[Ingredients] = relationship(back_populates="ingredients")

class CreateRecipeIngredientRequest(BaseModel):
    quantity: float = Field(gt=0)
    recipe_id: int
    ingredient_id: int
    
class RecipeIngredientResponse(BaseModel):
    id: int 
    quantity: float
    name: str = Field(..., alias='ingredient.name')
    unit: str = Field(..., alias='ingredient.unit')
    value: float
    
    model_config = ConfigDict(from_attributes=True)
    
    @classmethod
    def from_orm_with_value(cls, orm_obj):
        ingredient_value = orm_obj.ingredient.value
        calculated_value = ingredient_value * orm_obj.quantity
        return cls(
            id=orm_obj.id,
            quantity=orm_obj.quantity,
            name=orm_obj.ingredient.name, # type: ignore
            unit=orm_obj.ingredient.unit,
            value=calculated_value
        )