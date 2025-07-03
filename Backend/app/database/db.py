from pymongo import MongoClient
from dotenv import load_dotenv
import os
# Charger les variables d'environnement depuis .env
load_dotenv()
# Récupérer l'URI de connexion
MONGO_URI = os.getenv("MONGO_URI")
# Créer la connexion
client = MongoClient(MONGO_URI)
# Choisir la base de données
db = client["bioskin"]
# Exemple d'accès à une collection
users_collection = db["users"]
recipes_collection = db["recipes"]
favoris_collection = db["favoris"]
ingredients_collection = db["ingredients"]
zone_collection = db["zone"]
skin_types_collection = db["skin_type"]