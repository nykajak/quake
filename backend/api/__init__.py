import os

from flask import Flask
from flask_caching import Cache
from flask_mail import Mail
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from api.app_secrets import *

from api.database import db
from api import workers

# BASE_DIR denotes the /backend/api folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Flask specific settings
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = FLASK_SECRET_KEY

# FlaskSqlAlchemy settings
app.config["SQLITE_DB_DIR"] = os.path.join(BASE_DIR, "../instance")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.config["SQLITE_DB_DIR"],"quiz.db")

# Flask-jwt-extended settings
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

# Flask-mail settings
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'

# Celery settings
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'

# Cache settings
app.config["CACHE_TYPE"] = "redis"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 3

# Initialising JWT for auth
jwt = JWTManager(app)

# Initialising bcrypt for hashing
bcrypt = Bcrypt(app)

# Initialising flask_mail
mail = Mail(app)

# Initialising flask_cache
cache = Cache(app)
cache.init_app(app)

# Initialising flask_cors for cross site origin requests
CORS(app,supports_credentials=True)

# Intialising flask_sql_alchemy for db
db.init_app(app)

# Initialising celery for background jobs
celery = workers.celery
celery.conf.update(
    broker_url = app.config['CELERY_BROKER_URL'],
    result_backend = app.config['CELERY_RESULT_BACKEND'],
    timezone = 'Asia/Kolkata',
    enable_utc = False
)
celery.Task = workers.ContextTask

# Pushing app context
app.app_context().push()

# Importing all routes and tasks to make them accessible!
import api.routes
import api.tasks