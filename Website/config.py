import os

class Config:
    """Config of the app
    """
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = 'en'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    FLASK_ADMIN_SWATCH = 'superhero'
    GOOGLE_OAUTH_CLIENT_ID = "721867642124-4kco7ba22u6h90gc3d0hkok1bdv7eguk.apps.googleusercontent.com"
    GOOGLE_OAUTH_CLIENT_SECRET = "Q9NwbBSPqCULQg0rLTB5sdfT"
    GITHUB_OAUTH_CLIENT_ID = "b523d4fdf187588cb1cd"
    GITHUB_OAUTH_CLIENT_SECRET = "dc55b0b4b510321cbcff6febb84d30fcea0d5385"
    LANGUAGES = ['en', 'ru', 'de', 'es']