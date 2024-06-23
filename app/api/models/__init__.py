# models/__init__.py
from .recipe_sales import RecipeSales
from .recipes import Recipe
from .recipe_ingredients import RecipeIngredients
from sqlalchemy.orm import relationship

# Define relationships
Recipe.ingredients = relationship(RecipeIngredients, back_populates="recipe")
RecipeIngredients.recipe = relationship(Recipe, back_populates="ingredients")

RecipeSales.recipe = relationship(Recipe)