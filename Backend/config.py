import os
from dotenv import load_dotenv

load_dotenv()  # charge les variables depuis ton fichier .env

class Config:
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "une_clef_secrete_par_defaut")  # clé pour sécuriser Flask
    MONGO_URI = os.getenv("MONGO_URI")  # URI pour ta base MongoDB
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # clé API OpenAI

class DevelopmentConfig(Config):
    DEBUG = True  # active le mode debug en développement