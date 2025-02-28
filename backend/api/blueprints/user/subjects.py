from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required, get_current_user
from api.models import *
from api.blueprints.user import user_required

user_subject_routes = Blueprint('user_subject_routes', __name__)

@user_subject_routes.get("/all")
@jwt_required()
@user_required
def available_subjects():
    u = get_current_user()

    requested = [x.subject_id for x in Requested.query.all()]
    enrolled = [x.id for x in u.subjects]
    subjects = [x.serialise() for x in Subject.query.all()]
    subjects = [x for x in subjects if x["id"] not in enrolled and x["id"] not in requested]
    return jsonify(payload=subjects),200

@user_subject_routes.get("/")
@jwt_required()
@user_required
def user_subjects():
    u = get_current_user()
    return jsonify(payload=u.serialise('subjects')),200

@user_subject_routes.get("/<sid>")
@jwt_required()
@user_required
def user_specific_subject(sid):
    u = get_current_user()
    s = Subject.query.filter(Subject.id == sid).scalar()

    if s is None:
        return jsonify(msg = "Subject not found!"), 400
    
    if s not in u.subjects:
        return jsonify(msg = "User not registered for subject!"),400

    return jsonify(payload=s.serialise('chapters')),200