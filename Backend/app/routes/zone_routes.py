from flask import Blueprint, request, jsonify
from app.database.db import db
from bson.objectid import ObjectId


bp = Blueprint('zone_routes', __name__)
zones_collection = db["zones"]

@bp.route('/zones', methods=['GET'])
def get_zones():
    """
    Récupère toutes les zones dans la base de données.
    """
    zones = list(zones_collection.find())
    for zone in zones:
        zone['_id'] = str(zone['_id'])
    return jsonify(zones), 200

@bp.route('/zones', methods=['POST'])
def create_zone():
    """
    Crée une nouvelle zone dans la base de données.
    """
    data = request.json
    name = data.get('name')
    description = data.get('description', '')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    if zones_collection.find_one({"name": name}):
        return jsonify({"error": "Zone already exists"}), 409

    new_zone = {
        "name": name,
        "description": description,
    }

    result = zones_collection.insert_one(new_zone)
    new_zone['_id'] = str(result.inserted_id)

    return jsonify(new_zone), 201


@bp.route('/zones/<zone_id>', methods=['PUT'])
def update_zone(zone_id):
    """
    Met à jour une zone existante dans la base de données.
    """
    try:
        _id = ObjectId(zone_id)
    except Exception:
        return jsonify({"error": "Invalid zone ID"}), 400

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

    result = zones_collection.update_one({"_id": _id}, {"$set": update_fields})
    
    if result.matched_count == 0:
        return jsonify({"error": "Zone not found"}), 404

    return jsonify({"message": "Zone updated successfully"}), 200


@bp.route('/zones/<zone_id>', methods=['DELETE'])
def delete_zone(zone_id):
    """
    Supprime une zone de la base de données.
    """
    try:
        _id = ObjectId(zone_id)
    except Exception:
        return jsonify({"error": "Invalid zone ID"}), 400

    result = zones_collection.delete_one({"_id": _id})
    
    if result.deleted_count == 0:
        return jsonify({"error": "Zone not found"}), 404

    return jsonify({"message": "Zone deleted successfully"}), 200

