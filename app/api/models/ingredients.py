from dataclasses import field
from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy import DECIMAL, Date, Float, ForeignKey, Integer, func, Column
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

#from app.api.models.recipe_ingredients import RecipeIngredients

#from app.api.models.recipe_ingredients import RecipeIngredients


#from configs.database import Base

class Base(DeclarativeBase):
    pass

class Ingredients(Base):
    __tablename__="ingredient"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150))
    quantity = Column(Float)
    unit = Column(String(15))
    value = Column(Float)
    #recipe_ingredients = relationship("RecipeIngredient")
    created_at = Column(Date, default=func.now())
    updated_at = Column(Date, default=func.now(), onupdate=func.now())