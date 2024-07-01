# models/__init__.py
from app.api.models.recipe_sales_item import RecipeSalesItem
from .recipe_sales import RecipeSales
from .recipes import Recipe
from .recipe_ingredients import RecipeIngredients
from sqlalchemy.orm import relationship

# Define relationships
Recipe.ingredients = relationship(RecipeIngredients, back_populates="recipe")
RecipeIngredients.recipe = relationship(Recipe, back_populates="ingredients")

Recipe.sales_items = relationship(RecipeSalesItem, back_populates="recipe")

RecipeSalesItem.recipe_sale = relationship(RecipeSales, back_populates="items")
RecipeSalesItem.recipe = relationship(Recipe, back_populates="sales_items")

RecipeSales.items = relationship(RecipeSalesItem, back_populates="recipe_sale")

# RecipeSalesItem.recipe_sale = relationship(RecipeSales, back_populates="items")
# RecipeSales.items = relationship(RecipeSalesItem, back_populates="recipe_sale")
