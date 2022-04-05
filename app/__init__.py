import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.db import db
from app.models.user import User
from app.views.auth import auth
from app.views.products import products
from flask_migrate import Migrate
from app.seeders.seed import seed_db

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 86400

db.init_app(app)
Migrate(app, db)
CORS(app)
jwt = JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(products)

app.cli.add_command(seed_db, "seed_db")
