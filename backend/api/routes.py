from api import app,db,bcrypt,jwt
from api.models import *
from flask import request, jsonify
from flask_jwt_extended import jwt_required,current_user
from sqlalchemy.exc import IntegrityError

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter(User.name == identity).scalar()

@app.get("/")
@jwt_required(optional=True)
def home():
    if current_user:
        return jsonify(msg = f"Hello {current_user.name}!")
    
    return jsonify(msg="Hello anonymous person!")

from api.blueprints.anon.anon_routes import anon_routes
from api.blueprints.admin import admin_routes

app.register_blueprint(anon_routes)
app.register_blueprint(admin_routes,url_prefix="/admin")