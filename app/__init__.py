from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config.from_object(Config)

db = SQLAlchemy()
db.init_app(application)
migrate = Migrate(application, db)

from app import routes