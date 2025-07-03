from flask import Blueprint, request, jsonify
from app.database.db import db
from bson.objectid import ObjectId
from datetime import datetime

bp = Blueprint('history_routes', __name__)
history_collection = db["history"]

@bp.route('/history', methods=['POST'])
def add_history_entry():
    """
    Ajoute une entrée d'historique pour un utilisateur.
    """
    data = request.json
    user_id = data.get('user_id')
    recipe_id = data.get('recipe_id')
    timestamp = datetime.utcnow()

    if not user_id or not recipe_id:
        return jsonify({"error": "User ID and Recipe ID are required"}), 400

    history_entry = {
        "user_id": user_id,
        "recipe_id": recipe_id,
        "timestamp": timestamp
    }

    result = history_collection.insert_one(history_entry)
    history_entry['_id'] = str(result.inserted_id)

    return jsonify(history_entry), 201


@bp.route('/history/<user_id>', methods=['GET'])
def get_user_history(user_id):
    """
    Récupère l'historique des recettes consultées par un utilisateur.
    """
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    history_entries = list(history_collection.find({"user_id": user_id}))
    for entry in history_entries:
        entry['_id'] = str(entry['_id'])
        entry['timestamp'] = entry['timestamp'].isoformat()
    return jsonify(history_entries), 200


@bp.route('/history/<history_id>', methods=['DELETE'])
def delete_history_entry(history_id):
    """
    Supprime une entrée d'historique.
    """
    try:
        _id = ObjectId(history_id)
    except Exception:
        return jsonify({"error": "Invalid history ID"}), 400

    result = history_collection.delete_one({"_id": _id})
    if result.deleted_count == 0:
        return jsonify({"error": "History entry not found"}), 404

    return jsonify({"message": "History entry deleted successfully"}), 200