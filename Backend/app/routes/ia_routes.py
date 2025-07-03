from flask import Blueprint, request, jsonify
from app.database.db import db
from bson.objectid import ObjectId
import random
from app.services.ia_services import (
    get_compatible_recipes,
    save_generated_recipe,
    choose_random_recipe
)

bp = Blueprint('ia_routes', __name__)
ia_collection = db["ia"]
recipes_collection = db["recipes"]


@bp.route('/ia', methods=['POST'])
def generate_recipe():
    """
    Génère une recette basée sur les données de l'utilisateur.
    """
    data = request.json
    user_id = data.get('user_id')
    skin_type = data.get('skin_type')
    zone = data.get('zone')
    user_ingredients = data.get('ingredients', [])
    save = data.get('save', False)

    if not user_id or not skin_type or not zone:
        return jsonify({"error": "User ID, skin type, and zone are required"}), 400

    # Récupérer les recettes basées sur le type de peau et la zone
    recipes = list(recipes_collection.find({"skin_type": skin_type, "zone": zone}))

    if not recipes:
        return jsonify({"error": "No recipes found for the given skin type and zone"}), 404

# 2. Filtrer recettes avec uniquement les ingrédients disponibles
    compatible_recipes = []
    user_ingredients_set = set(user_ingredients)
    for recipe in recipes:
        recipe_ingredients_set = set(recipe.get('ingredients', []))
        if recipe_ingredients_set.issubset(user_ingredients_set):
            recipe['_id'] = str(recipe['_id'])
            compatible_recipes.append(recipe)

    if not compatible_recipes:
        return jsonify({"error": "No recipes match the available ingredients"}), 404

    # Sélectionner une recette compatible au hasard
    selected_recipe = random.choice(compatible_recipes)

    # Enregistrer l'entrée IA dans la collection
    ia_entry = {
        "user_id": user_id,
        "skin_type": skin_type,
        "zone": zone,
        "recipe_id": selected_recipe['_id'],
        "save": save
    }
    
    result = ia_collection.insert_one(ia_entry)
    ia_entry['_id'] = str(result.inserted_id)

    return jsonify({"recipe": selected_recipe, "ia_entry": ia_entry}), 201