class Config:
    """Config of the app
    """
    SECRET_KEY = "1f647c79ac3ac911bc3fcca76321ea2f"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = 'en'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "kirillswebsite@gmail.com"
    MAIL_PASSWORD = "nohacks1337"
    FLASK_ADMIN_SWATCH = 'cerulean'