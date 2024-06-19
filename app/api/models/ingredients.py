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


#from configs.database import Base

class Base(DeclarativeBase):
    pass

class Ingredients(Base):
    __tablename__="ingredient"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150))
    quantity: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(15))
    value: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())

class CreateIngredientRequest(BaseModel):
    name: str = Field(min_length=3, max_length=150)
    quantity: float = Field(gt=0)
    unit: str = Field(min_length=1)
    value: float = Field(gt=0)
    
class IngredientResponse(BaseModel):
    id: int 
    name: str
    quantity: float
    unit: str
    value: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)