
from sqlalchemy.orm import DeclarativeBase, declarative_base, relationship
from sqlalchemy import Column, Float, ForeignKey, Integer, UniqueConstraint

from app.api.models.ingredients import Ingredients
from app.api.models.recipes import Recipe

#from configs.database import Base

class Base(DeclarativeBase):
    pass

class RecipeIngredients(Base):
    __tablename__="recipe_ingredient"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    quantity = Column(Float)
    recipe_id = Column(Integer, ForeignKey(Recipe.id), nullable=False)
    ingredient_id = Column(Integer, ForeignKey(Ingredients.id), nullable=False)
    ingredients = relationship(Ingredients)
    
    __table_args__ = (UniqueConstraint('recipe_id', 'ingredient_id', name='recipe_ingredient_uc'),)
    
    
    #recipe = relationship("Recipe", back_populates="ingredients")