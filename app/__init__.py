from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config_file import Config
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"
login.refresh_view = 'login'

from app import routes
from app import models