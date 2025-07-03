
from flask import Blueprint, request, jsonify
from app.database.db import db
from bson.objectid import ObjectId

bp = Blueprint('ingredient_routes', __name__)
ingredients_collection = db["ingredients"]

@bp.route( '/ingredients', methods=['GET'])
def get_ingredients():
    """
    Récupère tous les ingrédients dans la base de données.
    """
    ingredients = list(ingredients_collection.find())
    for ingredient in ingredients:
        ingredient['_id'] = str(ingredient['_id'])
    return jsonify(ingredients), 200

@bp.route( '/ingredients', methods=['POST'])
def create_ingredient():
    """
    Crée un nouvel ingrédient dans la base de données.
    """
    data = request.json
    name = data.get('name')
    description = data.get('description', '')
    category = data.get('category', 'general')
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    if ingredients_collection.find_one({"name": name}):
        return jsonify({"error": "Ingredient already exists"}), 409
    
    new_ingredient = {
        "name": name,
        "description": description,
        "category": category,
    }
    result = ingredients_collection.insert_one(new_ingredient)
    new_ingredient['_id'] = str(result.inserted_id)
    return jsonify(new_ingredient), 201

@bp.route('/ingredients/<ingredient_id>', methods=['PUT'])
def update_ingredient(ingredient_id):
    """
    Met à jour un ingrédient existant dans la base de données.
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    update_fields = {}
    if 'name' in data:
        update_fields['name'] = data['name']
    if 'description' in data:
        update_fields['description'] = data['description']
    if 'category' in data:
        update_fields['category'] = data['category']
    
    if not update_fields:
        return jsonify({"error": "No fields to update"}), 400
    
    try:
        _id = ObjectId(ingredient_id)
    except Exception:
        return jsonify({"error": "Invalid ingredient ID"}), 400
    
    result = ingredients_collection.update_one(
        {"_id": _id},
        {"$set": update_fields}
    )
    
    if result.matched_count == 0:
        return jsonify({"error": "Ingredient not found"}), 404
    
    return jsonify({"message": "Ingredient updated successfully"}), 200

@bp.route('/ingredients/<ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    """
    Supprime un ingrédient de la base de données.
    """
    try:
        _id = ObjectId(ingredient_id)
    except Exception:
        return jsonify({"error": "Invalid ingredient ID"}), 400
    
    result = ingredients_collection.delete_one({"_id": _id})
    
    if result.deleted_count == 0:
        return jsonify({"error": "Ingredient not found"}), 404
    
    return jsonify({"message": "Ingredient deleted successfully"}), 200