from flask import Flask
from .ai_service import analyse_data
from .user_service import create_user, get_user
from services import create_user

def create_app():
