from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from app.main.views import views
    from app.main.errors import error
    from app.main.api import api

    app.register_blueprint(views)
    app.register_blueprint(error, url_prefix='/error')
    app.register_blueprint(api, url_prefix='/api')

    db.init_app(app)
    login_manager.init_app(app)

    return app
