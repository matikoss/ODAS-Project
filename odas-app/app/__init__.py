from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('ODAS_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SESSION_COOKIE_SAMESITE'] = "Strict"
    app.config['SESSION_COOKIE_SECURE'] = True

    db.init_app(app)
    limiter.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'main.start'
    login_manager.login_message_category = "danger"
    login_manager.session_protection = "strong"

    login_manager.init_app(app)

    from .models import User
    from .models import Note

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    return app
