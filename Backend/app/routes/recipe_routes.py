from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from app.database.db import db

bp = Blueprint('recipe_routes', __name__)
recipes_collection = db["recipes"]

@bp.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = list(recipes_collection.find())
    for recipe in recipes:
        recipe['_id'] = str(recipe['_id'])
    return jsonify(recipes), 200

@bp.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({"error": "Recipe name is required"}), 400
    
    new_recipe = {
        "name": data['name'],
        "description": data.get('description', ''),
        "ingredients": data.get('ingredients', []),  # liste d'IDs ou noms d'ingrédients
        "steps": data.get('steps', [])
    }
    
    result = recipes_collection.insert_one(new_recipe)
    new_recipe['_id'] = str(result.inserted_id)
    return jsonify(new_recipe), 201

@bp.route('/recipes/<recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    try:
        _id = ObjectId(recipe_id)
    except Exception:
        return jsonify({"error": "Invalid recipe ID"}), 400
    
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    update_fields = {}
    if 'name' in data:
        update_fields['name'] = data['name']
    if 'description' in data:
        update_fields['description'] = data['description']
    if 'ingredients' in data:
        update_fields['ingredients'] = data['ingredients']
    if 'steps' in data:
        update_fields['steps'] = data['steps']
    
    if not update_fields:
        return jsonify({"error": "No fields to update"}), 400
    
    result = recipes_collection.update_one({"_id": _id}, {"$set": update_fields})
    if result.matched_count == 0:
        return jsonify({"error": "Recipe not found"}), 404
    
    return jsonify({"message": "Recipe updated successfully"}), 200

@bp.route('/recipes/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    try:
        _id = ObjectId(recipe_id)
    except Exception:
        return jsonify({"error": "Invalid recipe ID"}), 400
    
    result = recipes_collection.delete_one({"_id": _id})
    if result.deleted_count == 0:
        return jsonify({"error": "Recipe not found"}), 404
    
    return jsonify({"message": "Recipe deleted successfully"}), 200
