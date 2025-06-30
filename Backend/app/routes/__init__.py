from .user_routes import bp as user_bp
from .ai_routes import bp as ai_bp

def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(ai_bp)