# run.py

from flask import Flask
from config import DevelopmentConfig

# Import des blueprints
from app.routes.user_routes import bp as user_bp
from app.routes.favoris_routes import bp as favoris_bp
from app.routes.ingredient_routes import bp as ingredient_bp
from app.routes.recipe_routes import bp as recipe_bp


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Enregistrement des routes (blueprints)
app.register_blueprint(user_bp, url_prefix="/api/users")
app.register_blueprint(favoris_bp, url_prefix="/api/favoris")
app.register_blueprint(ingredient_bp, url_prefix="/api/ingredients")
app.register_blueprint(recipe_bp, url_prefix="/api/recipes")
# Ajoute d'autres enregistrements ici

if __name__ == "__main__":
    app.run(debug=True)
