from dataclasses import field
from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, Integer, func
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.api.models.user import User

# from api.models.recipe_ingredients import RecipeIngredients

#from configs.database import Base

class Base(DeclarativeBase):
    pass

class Recipe(Base):
    __tablename__="recipe"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    name: Mapped[str] = mapped_column(String(150))
    prep_time: Mapped[str] = mapped_column(String(10))
    servings: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())
    
class CreateRecipeRequest(BaseModel):
    name: str = Field(min_length=3, max_length=150)
    prep_time: str = Field(min_length=2, max_length=10)
    servings: int = Field(gt=0)
    
class RecipeResponse(BaseModel):
    id: int 
    user_id: int
    name: str
    prep_time: str
    servings: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PartialUpdateRecipeRequest(BaseModel):
    name: Optional[str] = None
    prep_time: Optional[str] = None
    servings: Optional[int] = None