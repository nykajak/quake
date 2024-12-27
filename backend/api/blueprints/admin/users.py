from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required

user_routes = Blueprint('user_routes', __name__)

@user_routes.get("/")
@jwt_required()
@admin_required
def all_users():
    page = int(request.args.get("page",1))
    per_page = int(request.args.get("per_page",1))
    
    res = []
    for u in User.query.filter().paginate(page=page,per_page=per_page):
        res.append({"name" : u.name})
    
    return jsonify(payload=res)