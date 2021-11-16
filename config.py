import os
from dotenv import load_dotenv
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    CKEDITOR_SERVE_LOCAL = False
    CKEDITOR_PKG_TYPE = 'full'
    UPLOAD_FOLDER = os.path.join(BASE_DIR, os.getenv('UPLOAD_DIR'))
    ALLOWED_EXTENSIONS = os.getenv('ALLOWED_IMG_EXTENSTIONS')
    PER_PAGE = os.getenv('PAGINATION_PER_PAGE')

class developmentConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_ECHO = False

class productionConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_ECHO = False

config = {
    "development" : developmentConfig,
    "production" : productionConfig
}

app_config = config[os.getenv('MODE')]
