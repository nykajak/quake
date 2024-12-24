import os
from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from api.database import db

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config["SQLITE_DB_DIR"] = os.path.join(BASE_DIR, "../instance")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.config["SQLITE_DB_DIR"],"quiz.db")
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app,supports_credentials=True)
db.init_app(app)
app.app_context().push()

import api.routes