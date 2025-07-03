from .user_service import (
    create_user,
    get_user_by_id,
    get_user_by_email
)
from .ia_services import (
    get_compatible_recipes,
    save_generated_recipe,
    choose_random_recipe
)
from .favoris_service import (
    add_favori,
    get_favoris_by_user,
    remove_favori
)
from .ingredient_service import (
    get_all_ingredients,
    get_ingredient_by_id,
    add_ingredient,
    delete_ingredient
)
from app.database.db import db
from .zone_service import ZoneService

zone_service = ZoneService(db)
list_zones = zone_service.list_zones  # Permet d'utiliser list_zones comme fonction

from .skin_type_service import SkinTypeService
skin_type_service = SkinTypeService(db)
list_skin_types = skin_type_service.list_skin_types  # Permet d'utiliser list_skin_types as fonction

from .recipe_service import RecipeService
recipe_service = RecipeService(db)
generate_recipe = recipe_service.generate_recipe  # Permet d'utiliser generate_recipe comme fonction