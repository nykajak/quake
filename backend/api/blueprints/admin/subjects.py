from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required

subject_routes = Blueprint('subject_routes', __name__)

@subject_routes.get("/")
@jwt_required()
@admin_required
def all_subjects():
    page = int(request.args.get("page",1))
    per_page = int(request.args.get("per_page",5))

    query = Subject.query.filter().paginate(page=page,per_page=per_page,max_per_page=10)
    res = [s.serialise() for s in query]
    
    return jsonify(payload=res)

@subject_routes.get("/<id>")
@jwt_required()
@admin_required
def specific_subjects(id):
    s = Subject.query.filter(Subject.id == id).scalar()
    if s:
        return jsonify(payload=s.serialise())
    
    return jsonify(msg="No such subject found!"),400