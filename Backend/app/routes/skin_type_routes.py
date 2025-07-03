from flask import Blueprint, request, jsonify
from app.database.db import db
from bson.objectid import ObjectId

bp = Blueprint('skin_type_routes', __name__)
skin_types_collection = db["skin_types"]

@bp.route('/skin_types', methods=['GET'])
def get_skin_types():
    """
    Récupère tous les types de peau dans la base de données.
    """
    skin_types = list(skin_types_collection.find())
    for skin_type in skin_types:
        skin_type['_id'] = str(skin_type['_id'])
    return jsonify(skin_types), 200

@bp.route('/skin_types', methods=['POST'])
def create_skin_type():
    """
    Crée un nouveau type de peau dans la base de données.
    """
    data = request.json
    name = data.get('name')
    description = data.get('description', '')
    
    if not name:
        return jsonify({"error": "Name is required"}), 400
    
    if skin_types_collection.find_one({"name": name}):
        return jsonify({"error": "Skin type already exists"}), 409
    
    new_skin_type = {
        "name": name,
        "description": description,
    }
    
    result = skin_types_collection.insert_one(new_skin_type)
    new_skin_type['_id'] = str(result.inserted_id)
    
    return jsonify(new_skin_type), 201

@bp.route('/skin_types/<skin_type_id>', methods=['PUT'])
def update_skin_type(skin_type_id):
    """
    Met à jour un type de peau existant dans la base de données.
    """
    try:
        _id = ObjectId(skin_type_id)
    except Exception:
        return jsonify({"error": "Invalid skin type ID"}), 400
    
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    update_fields = {}
    if 'name' in data:
        update_fields['name'] = data['name']
    if 'description' in data:
        update_fields['description'] = data['description']
    
    if not update_fields:
        return jsonify({"error": "No fields to update"}), 400
    
    result = skin_types_collection.update_one({"_id": _id}, {"$set": update_fields})
    if result.matched_count == 0:
        return jsonify({"error": "Skin type not found"}), 404
    
    return jsonify({"message": "Skin type updated successfully"}), 200

@bp.route('/skin_types/<skin_type_id>', methods=['DELETE'])
def delete_skin_type(skin_type_id):
    """
    Supprime un type de peau de la base de données.
    """
    try:
        _id = ObjectId(skin_type_id)
    except Exception:
        return jsonify({"error": "Invalid skin type ID"}), 400
    
    result = skin_types_collection.delete_one({"_id": _id})
    if result.deleted_count == 0:
        return jsonify({"error": "Skin type not found"}), 404
    
    return jsonify({"message": "Skin type deleted successfully"}), 200