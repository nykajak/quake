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
    per_page = int(request.args.get("per_page",5))

    query = User.query.filter().paginate(page=page,per_page=per_page,max_per_page=10)
    res = [u.serialise() for u in query]
    
    return jsonify(payload=res)

@user_routes.get("/<name>")
@jwt_required()
@admin_required
def specific_users(name):
    u = User.query.filter(User.name == name).scalar()
    if u:
        return jsonify(payload=u.serialise())
    return jsonify(msg="No such user found!"),400