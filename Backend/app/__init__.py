from flask import Flask
from .database.db import db
from .routes import user_routes, ai_routes

def create_app():
    app = Flask(__name__)

    app.config.from_object('config')
    
    db.init_db(app)

    app.register_blueprint(user_routes.bp)
    app.register_blueprint(ai_routes.bp)

    return app
