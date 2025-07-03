from .user_routes import bp as user_bp
from .ia_routes import bp as ia_bp
from .favoris_routes import bp as favoris_bp
from .ingredient_routes import bp as ingredient_bp
from .zone_routes import bp as zone_bp
from .recipe_routes import bp as recipe_bp
from .history_routes import bp as history_bp
from .skin_type_routes import bp as skin_type_bp 


def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(ia_bp)
    app.register_blueprint(favoris_bp)
    app.register_blueprint(ingredient_bp)
    app.register_blueprint(zone_bp)
    app.register_blueprint(skin_type_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(history_bp)