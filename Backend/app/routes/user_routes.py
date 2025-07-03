# File: Backend/app/routes/user_routes.py
from flask import request, jsonify  
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from app.database.db import db
# Import necessary modules

bp = Blueprint('user_routes', __name__)
users_collection = db["users"]

@bp.route('/create_user', methods=['POST'])
def create_user():
    # Logic to create a user
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return "Username and password are required", 400

    if users_collection.find_one({"username": username}):
        return "User already exists", 409
    
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({
        "username": username,
        "password": hashed_password
    })
    return jsonify({"message": "User created successfully"}), 201

@bp.route('/login', methods=['POST'])
def login():
    # Logic to log in a user
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return "Username and password are required", 400
    
    user = users_collection.find_one({"username": username})
    if not user or not check_password_hash(user['password'], password):
        return "Invalid credentials", 401
    return jsonify({"message": "Login successful"}), 200

@bp.route('/profile', methods=['GET'])
def profile():
    # Logic to get user profile
    username = request.args.get('username')
    if username is None:
        return "Username is required", 400
    
    user = users_collection.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "username": user['username']
    }), 200
    
@bp.route('/update_profile', methods=['PUT'])
def update_profile():
    # 1.Recuperer les données envoyees 
    
    username = request.json.get('username')
    new_password =request.json.get('new_password')
    new_username = request.json.get('new_username')
    
    # 2.Verification des champs obligatoires
    if not username:
        return jsonify({"error": "Username is required"}), 400
    if not new_username and not new_password:
        return jsonify({"error": "At least one field to update is required"}), 400
    
    # 3.Acces à la base de données
    user = users_collection.find_one({"username":username})
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    #4. Construction de la requete de mise à jour
    update_data = {}
    if new_password:
        update_data["password"] = generate_password_hash(new_password)
    if new_username:
        if users_collection.find_one({"username": new_username}):
            return jsonify({"error": "New username already exists"}), 409
        update_data["username"] = new_username
    # 5. Mise à jour du profil
    if update_data:
        users_collection.update_one({"username": username}, {"$set": update_data})
        
    return jsonify({"message": "Profile updated successfully"}), 200

@bp.route('/delete_user', methods=['DELETE'])
def delete_user():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    user = users_collection.find_one({"username": username})
    if not user or not check_password_hash(user['password'], password):return jsonify({"error": "Invalid credentials"}), 401
    users_collection.delete_one({"username": username})
    return jsonify({"message": "User deleted successfully"}), 200
