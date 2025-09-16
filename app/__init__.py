"""Base Flask app"""
import importlib
import os
from flask import Flask
from app.views import base_app, base_app_buying


def create_app(test_config=None):
    """Create and configure Flask app"""

    app = Flask(__name__)

    app.register_blueprint(base_app)
    app.register_blueprint(base_app_buying)

    return app