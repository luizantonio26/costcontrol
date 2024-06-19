from dataclasses import field
from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, func
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

#from app.utils import partial_model

#from configs.database import Base

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__="user_account"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    birthdate: Mapped[datetime] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())


class RegisterUserRequest(BaseModel):
    name: str = Field(max_length=30)
    email: str = Field(min_length=5, max_length=100)
    password: str = Field(min_length=6, max_length=24)
    confirm_password: str = Field(min_length=6, max_length=24)
    birthdate: datetime

#@partial_model
class UpdateUserRequest(BaseModel):
    name: str = Field(max_length=30)
    birthdate: datetime

class RegisterUserResponse(BaseModel):
    id: int
    name: str
    email: str
    birthdate: datetime
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class LoginUserRequest(BaseModel):
    email: str
    password: str
    
class LoginUserResponse(BaseModel):
    user: RegisterUserResponse
    tokens: dict