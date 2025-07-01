# run.py

from flask import Flask
from config import DevelopmentConfig

# Import des blueprints
from app.routes.user_routes import user_routes
from app.routes.favorite_routes import favorite_routes
from app.routes.ingredient_routes import ingredient_routes
from app.routes.recipe_routes import recipe_routes


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Enregistrement des routes (blueprints)
app.register_blueprint(user_routes, url_prefix="/api/users")
app.register_blueprint(favorite_routes, url_prefix="/api/favorites")
app.register_blueprint(ingredient_routes, url_prefix="/api/ingredients")
app.register_blueprint(recipe_routes, url_prefix="/api/recipes")
# Ajoute d'autres enregistrements ici

if __name__ == "__main__":
    app.run(debug=True)
