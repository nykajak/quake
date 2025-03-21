import os
from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from celery import Celery
from api.database import db
from api import workers

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config["SQLITE_DB_DIR"] = os.path.join(BASE_DIR, "../instance")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.config["SQLITE_DB_DIR"],"quiz.db")
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

# To be changed: Per instance basis for mail
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'f4e30739ab6564'
app.config['MAIL_PASSWORD'] = '39722368c4cadc'
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'

# Celery settings
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'

jwt = JWTManager(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
celery = workers.celery
celery.conf.update(
    broker_url = app.config['CELERY_BROKER_URL'],
    result_backend = app.config['CELERY_RESULT_BACKEND'],
    timezone = 'Asia/Kolkata',
    enable_utc = False
)

celery.Task = workers.ContextTask

CORS(app,supports_credentials=True)
db.init_app(app)
app.app_context().push()

import api.routes
import api.tasks
# Rewrite this file to support multiple config types