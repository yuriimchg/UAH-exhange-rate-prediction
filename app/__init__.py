from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.configs import app_config
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(app_config)
migrate = Migrate(app, db)

# Imports
from app import routes, db_models

