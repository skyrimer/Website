from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, gettext
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_view_counter import ViewCounter
from flask_admin import Admin
from Website.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
babel = Babel()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
title = gettext("Kirill's website")
pyowm_key = '71d9ed78c7a74fa1704089437d5e01f8'
admin = Admin(name=title)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['en', 'ru', 'de', 'es'])

    
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
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(features)
    return app
