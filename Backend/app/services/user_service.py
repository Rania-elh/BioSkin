# On importe MongoClient pour se connecter à MongoDB
from pymongo import MongoClient

# On importe ObjectId pour manipuler les identifiants MongoDB
from bson.objectid import ObjectId

# On importe notre configuration pour récupérer l'URI de la base
from config import Config

# On crée une connexion à la base MongoDB grâce à l'URI dans la config
client = MongoClient(Config.MONGO_URI)

# On sélectionne la base de données bioskin_db
db = client['bioskin_db']

# On cible la collection 'users' dans cette base
users_collection = db['users']

def create_user(user_data):
    """
    Fonction pour créer un nouvel utilisateur.
    user_data : dictionnaire contenant les infos du user (email, nom, mot de passe, etc.)
    """
    # On vérifie si un utilisateur avec le même email existe déjà
    existing_user = users_collection.find_one({"email": user_data.get("email")})
    if existing_user:
        # Si oui, on renvoie une erreur pour dire que l'email est déjà pris
        return {"error": "Email déjà utilisé"}, 400

    # Sinon, on insère le nouvel utilisateur dans la base
    result = users_collection.insert_one(user_data)

    # On renvoie un message de succès avec l'ID du nouvel utilisateur
    return {"message": "Utilisateur créé", "user_id": str(result.inserted_id)}, 201

def get_user_by_email(email):
    """
    Fonction pour retrouver un utilisateur grâce à son email.
    """
    # Recherche dans la collection 'users' d'un document avec cet email
    user = users_collection.find_one({"email": email})

    # Si aucun utilisateur trouvé, on renvoie None
    if not user:
        return None

    # On convertit l'_id de MongoDB (format spécial) en chaîne pour l'utiliser facilement
    user["_id"] = str(user["_id"])
    return user

def get_user_by_id(user_id):
    """
    Fonction pour retrouver un utilisateur grâce à son ID MongoDB.
    """
    try:
        # On convertit l'ID reçu (string) en ObjectId (format MongoDB)
        user = users_collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        # Si l'ID n'est pas valide (erreur de conversion), on renvoie None
        return None

    # Si aucun utilisateur trouvé avec cet ID, on renvoie None
    if not user:
        return None

    # Convertir l'ID en string pour pouvoir le manipuler facilement
    user["_id"] = str(user["_id"])
    return user
