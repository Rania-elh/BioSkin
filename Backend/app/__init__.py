from flask import Flask
from .database.db import db
from .routes import register_routes

def create_app():
    app = Flask(__name__)

    app.config.from_object('config')
    
    db.init_db(app)
    register_routes(app)

    return app
