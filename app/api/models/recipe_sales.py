from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Date, ForeignKey, Integer, Column, func
from sqlalchemy import String


from app.api.models.recipes import Recipe
from app.api.models.user import User

class Base(DeclarativeBase):
    pass

class RecipeSales(Base):
    __tablename__="recipe_sales"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id))
    client_name = Column(String(150))
    payment_method = Column(String)
    payment_status = Column(String)
    sale_date = Column(Date)
    created_at = Column(Date, default=func.now())
    updated_at = Column(Date, default=func.now(), onupdate=func.now())
    
    #ingredients = relationship("RecipeIngredients", back_populates="recipe")