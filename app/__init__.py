# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

SQLALCHEMY_TRACK_MODIFICATIONS = False # PV: becausee SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead

def create_app():
    app = Flask(__name__)

    # Load the config file
    app.config.from_object('config')

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprint for auth & non-auth routes in our app
    from .viewsAuth import auth as auth_blueprint
    from .viewsMain import main as main_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    # IMPORTANT - retourner la variable "app" pour qu'elle soit disponible dans le programme appelant
    return app
