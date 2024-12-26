from flask import Blueprint,jsonify
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required

user_routes = Blueprint('user_routes', __name__)

@user_routes.get("/")
@jwt_required()
@admin_required
def all_users():
    res = [] 
    for u in User.query.filter():
        res.append({"name" : u.name})
    
    return jsonify(payload=res)