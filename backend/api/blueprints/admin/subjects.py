from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required
from sqlalchemy.exc import IntegrityError

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

@subject_routes.post("/")
@jwt_required()
@admin_required
def add_subject():
    name = request.form.get("name",None)
    description = request.form.get("description",None)
    credits = int(request.form.get("credits",0))

    if credits == 0 or name is None:
        return jsonify(msg="Malformed request: Check if all fields included"),400
    
    s = None
    if description is None:
        s = Subject(name = name,credits = credits)
    else:
        s = Subject(name = name,credits = credits, description = description)

    try:
        db.session.add(s)
        db.session.commit()
        return jsonify(msg="Subject creation successful"),200
    
    except IntegrityError as e:
        return jsonify(msg="Name is not unique!"),400
