from pymongo import MongoClient
from bson.objectid import ObjectId
from config import Config

# Connexion à la base MongoDB
client = MongoClient(Config.MONGO_URI)
db = client['bioskin_db']

# Collection pour les ingrédients
ingredients_collection = db['ingredients']

def add_ingredient(name, description=None):
    """
    Ajoute un nouvel ingrédient.
    name : nom de l'ingrédient
    description : description optionnelle
    """
    # Vérifie si un ingrédient avec le même nom existe déjà
    existing = ingredients_collection.find_one({"name": name})
    if existing:
        return {"error": "Ingrédient déjà existant"}, 400

    # Création du document ingrédient
    ingredient_data = {"name": name}
    if description:
        ingredient_data["description"] = description

    # Insère l'ingrédient dans la base
    result = ingredients_collection.insert_one(ingredient_data)
    return {"message": "Ingrédient ajouté", "ingredient_id": str(result.inserted_id)}, 201

def get_all_ingredients():
    """
    Récupère la liste de tous les ingrédients.
    """
    ingredients = ingredients_collection.find()
    result = []
    for ing in ingredients:
        ing["_id"] = str(ing["_id"])
        result.append(ing)
    return result

def get_ingredient_by_id(ingredient_id):
    """
    Récupère un ingrédient par son ID.
    """
    ing = ingredients_collection.find_one({"_id": ObjectId(ingredient_id)})
    if not ing:
        return None
    ing["_id"] = str(ing["_id"])
    return ing

def delete_ingredient(ingredient_id):
    """
    Supprime un ingrédient par son ID.
    """
    result = ingredients_collection.delete_one({"_id": ObjectId(ingredient_id)})
    if result.deleted_count == 0:
        return {"error": "Ingrédient non trouvé"}, 404
    return {"message": "Ingrédient supprimé"}, 200
