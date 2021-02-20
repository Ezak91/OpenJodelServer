from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from .config import config_by_name

DB = SQLAlchemy()
FLASK_BCRYPT = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    DB.init_app(app)
    FLASK_BCRYPT.init_app(app)

    return app