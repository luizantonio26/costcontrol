from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Date, ForeignKey, Integer, Column, func
from sqlalchemy import String

from app.api.models.recipe_sales import RecipeSales
from app.api.models.recipes import Recipe

class Base(DeclarativeBase):
    pass

class RecipeSalesItem(Base):
    __tablename__="recipe_sales_items"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    recipe_sales_id = Column(Integer, ForeignKey(RecipeSales.id))
    recipe_id = Column(Integer, ForeignKey(Recipe.id))
    quantity = Column(Integer)
    created_at = Column(Date, default=func.now())
    updated_at = Column(Date, default=func.now(), onupdate=func.now())
    
    recipe = relationship(Recipe)
    #ingredients = relationship("RecipeIngredients", back_populates="recipe")