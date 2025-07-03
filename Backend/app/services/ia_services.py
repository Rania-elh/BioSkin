from app.database.db import db
import random

recipes_collection = db["recipes"]
ia_collection = db["ia"]

def get_compatible_recipes(user_ingredients, skin_type, zone):
    """
    Récupère les recettes compatibles avec les ingrédients de l'utilisateur,
    le type de peau et la zone.
    """
    recipes = list(recipes_collection.find({"skin_type": skin_type, "zone": zone}))

    if not recipes:
        return []

    compatible_recipes = []
    user_ingredients_set = set(user_ingredients)
    
    for recipe in recipes:
        recipe_ingredients_set = set(recipe.get('ingredients', []))
        if recipe_ingredients_set.issubset(user_ingredients_set):
            recipe['_id'] = str(recipe['_id'])
            compatible_recipes.append(recipe)

    return compatible_recipes

def save_generated_recipe(user_id, skin_type, zone, selected_recipe, save):
    """
    Enregistre l'entrée IA dans la collection.
    """
    ia_entry = {
        "user_id": user_id,
        "skin_type": skin_type,
        "zone": zone,
        "recipe_id": selected_recipe['_id'],
        "save": save
    }
    
    result = ia_collection.insert_one(ia_entry)
    ia_entry['_id'] = str(result.inserted_id)
    
    return ia_entry

def choose_random_recipe(compatible_recipes):
    """
    Sélectionne une recette compatible au hasard.
    """
    if not compatible_recipes:
        return None
    return random.choice(compatible_recipes)