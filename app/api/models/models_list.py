from app.api.models.recipe_sales_item import RecipeSalesItem
from app.api.models.security_settings import SecuritySettings
from app.api.models.user import User
from app.api.models.ingredients import Ingredients
from app.api.models.recipe_ingredients import RecipeIngredients
from app.api.models.recipes import Recipe
from app.api.models.recipe_sales import RecipeSales

custom_target_metadata = [
    User.metadata,
    Recipe.metadata,
    Ingredients.metadata,
    RecipeIngredients.metadata,
    RecipeSales.metadata,
    SecuritySettings.metadata,
    RecipeSalesItem.metadata
]
