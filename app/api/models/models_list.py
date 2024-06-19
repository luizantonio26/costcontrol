from api.models.user import User
from api.models.ingredients import Ingredients
from api.models.recipe_ingredients import RecipeIngredients
from api.models.recipes import Recipe

custom_target_metadata = [
    User.metadata,
    Recipe.metadata,
    Ingredients.metadata,
    RecipeIngredients.metadata,
]
