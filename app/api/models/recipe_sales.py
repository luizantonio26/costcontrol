from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Date, ForeignKey, Integer, Column, func
from sqlalchemy import String

from app.api.models.recipes import Recipe

class Base(DeclarativeBase):
    pass

class RecipeSales(Base):
    __tablename__="recipe_sales"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    recipe_id = Column(ForeignKey(Recipe.id))
    client_name = Column(String(150))
    quantity = Column(Integer)
    sale_date = Column(Date)
    created_at = Column(Date, default=func.now())
    updated_at = Column(Date, default=func.now(), onupdate=func.now())
    
    #ingredients = relationship("RecipeIngredients", back_populates="recipe")