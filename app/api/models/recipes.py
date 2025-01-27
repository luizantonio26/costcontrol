from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Date, ForeignKey, Integer, Column, func
from sqlalchemy import String

from app.api.models.user import User

# from api.models.recipe_ingredients import RecipeIngredients

#from configs.database import Base

class Base(DeclarativeBase):
    pass

class Recipe(Base):
    __tablename__="recipe"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(ForeignKey(User.id))
    image_url = Column(String(2400), nullable=True)
    name = Column(String(150))
    prep_time = Column(String(10))
    servings = Column(Integer)
    created_at = Column(Date, default=func.now())
    updated_at = Column(Date, default=func.now(), onupdate=func.now())
    
    #ingredients = relationship("RecipeIngredients", back_populates="recipe")