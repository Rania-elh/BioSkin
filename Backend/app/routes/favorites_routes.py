from flask import Blueprint, request, jsonify
from app.database.db import db
from bson.objectid import ObjectId

bp = Blueprint('favorites_routes', __name__)
favorites_collection = db["favorites"]

@bp.route('/favorites', methods=['POST'])
def add_favorite():
    """

    """
    data = request.json
    user_id = data.get('user_id')
    recipe_id = data.get('recipe_id')

    if not user_id or not recipe_id:
        return jsonify({"error": "User ID and Recipe ID are required"}), 400
    
    existing_favorite = favorites_collection.find_one({
        "user_id": user_id,
        "recipe_id": recipe_id
    })
    if existing_favorite:
        return jsonify({"error": "Recipe already in favorites"}), 409

    favorite = {
        "user_id": user_id,
        "recipe_id": recipe_id
    }

    result = favorites_collection.insert_one(favorite)
    favorite['_id'] = str(result.inserted_id)

    return jsonify(favorite), 201

@bp.route('/favorites/<user_id>', methods=['GET'])
def get_favorites(user_id):
    """
    Récupère tous les favoris d'un utilisateur.
    """
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    favorites = list(favorites_collection.find({"user_id": user_id}))
    for favorite in favorites:
        favorite['_id'] = str(favorite['_id'])

    return jsonify(favorites), 200

@bp.route('/favorites/<favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    """
    Supprime une recette des favoris de l'utilisateur.
    """
    try:
        _id = ObjectId(favorite_id)
    except Exception:
        return jsonify({"error": "Invalid favorite ID"}), 400

    result = favorites_collection.delete_one({"_id": _id})
    if result.deleted_count == 0:
        return jsonify({"error": "Favorite not found"}), 404

    return jsonify({"message": "Favorite deleted successfully"}), 200