from flask import Blueprint, request, jsonify
from app.database.db import db
from bson.objectid import ObjectId

bp = Blueprint('favoris_routes', __name__)
favoris_collection = db["favoris"]

@bp.route('/favoris', methods=['POST'])
def add_favori():
    """
    """
    data = request.json or {}
    user_id = data.get('user_id')
    recipe_id = data.get('recipe_id')

    if not user_id or not recipe_id:
        return jsonify({"error": "User ID and Recipe ID are required"}), 400
    
    existing_favori = favoris_collection.find_one({
        "user_id": user_id,
        "recipe_id": recipe_id
    })
    if existing_favori:
        return jsonify({"error": "Recipe already in favoris"}), 409

    favori = {
        "user_id": user_id,
        "recipe_id": recipe_id
    }

    result = favoris_collection.insert_one(favori)
    favori['_id'] = str(result.inserted_id)

    return jsonify(favori), 201

@bp.route('/favoris/<user_id>', methods=['GET'])
def get_favoris(user_id):
    """
    Récupère tous les favoris d'un utilisateur.
    """
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    favoris = list(favoris_collection.find({"user_id": user_id}))
    for favori in favoris:
        favori['_id'] = str(favori['_id'])

    return jsonify(favoris), 200

@bp.route('/favoris/<favori_id>', methods=['DELETE'])
def delete_favori(favori_id):
    """
    Supprime une recette des favoris de l'utilisateur.
    """
    try:
        _id = ObjectId(favori_id)
    except Exception:
        return jsonify({"error": "Invalid favori ID"}), 400

    result = favoris_collection.delete_one({"_id": _id})
    if result.deleted_count == 0:
        return jsonify({"error": "Favori not found"}), 404

    return jsonify({"message": "Favori deleted successfully"}), 200