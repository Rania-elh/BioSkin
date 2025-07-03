from pymongo import MongoClient
from bson.objectid import ObjectId
from config import Config

# Connexion à MongoDB
client = MongoClient(Config.MONGO_URI)
db = client['bioskin_db']

# Collection pour les favoris
favoris_collection = db['favoris']

def add_favori(user_id, recipe_id):
    """
    Ajoute une recette aux favoris d'un utilisateur.
    user_id : ID de l'utilisateur (string)
    recipe_id : ID de la recette (string)
    """
    # Vérifie si ce favori existe déjà pour éviter les doublons
    existing = favoris_collection.find_one({
        "user_id": ObjectId(user_id),
        "recipe_id": ObjectId(recipe_id)
    })
    if existing:
        return {"error": "Recette déjà en favoris"}, 400

    # Insère le favori (liens user + recette)
    result = favoris_collection.insert_one({
        "user_id": ObjectId(user_id),
        "recipe_id": ObjectId(recipe_id)
    })
    return {"message": "Favori ajouté", "favori_id": str(result.inserted_id)}, 201

def get_favoris_by_user(user_id):
    """
    Récupère toutes les recettes favoris d'un utilisateur.
    """
    # Trouve tous les favoris pour cet utilisateur
    favoris = favoris_collection.find({"user_id": ObjectId(user_id)})

    # Transforme le résultat en liste avec conversion des IDs en string
    result = []
    for fav in favoris:
        fav["_id"] = str(fav["_id"])
        fav["user_id"] = str(fav["user_id"])
        fav["recipe_id"] = str(fav["recipe_id"])
        result.append(fav)

    return result

def remove_favori(user_id, recipe_id):
    """
    Supprime une recette des favoris d'un utilisateur.
    """
    # Supprime le favori correspondant au user et à la recette
    result = favoris_collection.delete_one({
        "user_id": ObjectId(user_id),
        "recipe_id": ObjectId(recipe_id)
    })
    if result.deleted_count == 0:
        return {"error": "Favori non trouvé"}, 404

    return {"message": "Favori supprimé"}, 200
