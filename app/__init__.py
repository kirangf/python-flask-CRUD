from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from config import app_config

app = Flask(__name__)
app.config.from_object(app_config)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.message = "You must be logged in to access this page."
login_manager.login_view = 'auth.login'

ckeditor = CKEditor(app)

import error_handler
import register_modules

db.create_all()