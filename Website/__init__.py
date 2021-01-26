from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_view_counter import ViewCounter
from flask_admin import Admin
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.github import make_github_blueprint, github
from Website.config import Config
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
title = "Kirill's website"
db = SQLAlchemy()
bcrypt = Bcrypt()
babel = Babel()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
admin = Admin(name=title)
pyowm_key = os.environ.get('PYOWM_KEY')
languages = Config.LANGUAGES
google_blueprint = make_google_blueprint(
    scope=["https://www.googleapis.com/auth/userinfo.email", "openid", "https://www.googleapis.com/auth/userinfo.profile"])
github_blueprint = make_github_blueprint()


@babel.localeselector
def get_locale():
    if current_user.is_authenticated:
        return current_user.language
    else:
        return request.accept_languages.best_match(languages)


def create_app(config_class=Config):
    global views
    """Creating the main app

    Args:
        config_class (optional): configuration class. Defaults to Config.

    Returns:
        app: main app
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)
    with app.app_context():
        views = ViewCounter(app, db)

    from Website.users.routes import users
    from Website.posts.routes import posts
    from Website.main.routes import main
    from Website.erorrs.handlers import errors
    from Website.features.routes import features

    app.register_blueprint(google_blueprint, url_prefix="/google_login")
    app.register_blueprint(github_blueprint, url_prefix="/github_login")
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(features)
    return app
