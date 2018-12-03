from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.configs import app_config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('configs/app_config.py', silent=False)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Imports
from app import routes, db_models

