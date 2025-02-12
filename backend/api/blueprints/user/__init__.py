from functools import wraps
from flask import jsonify,Blueprint
from flask_jwt_extended import get_current_user, jwt_required
from api.models import *

user_routes = Blueprint('user_routes', __name__)

def user_required(fun):
    @wraps(fun)
    def inner(*args,**kwargs):
        current_user = get_current_user()
        if current_user.is_admin == 0:
            return fun(*args,**kwargs)
        return jsonify(msg="Not a user!"),400
    return inner

@user_routes.get("/")
@jwt_required()
@user_required
def profile():
    u = get_current_user()
    return jsonify(payload=u.serialise()),200

@user_routes.get("/subjects")
@jwt_required()
@user_required
def user_subjects():
    u = get_current_user()
    return jsonify(payload=u.serialise('subjects')),200

@user_routes.get("/subjects/<sid>")
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

@user_routes.get("/subjects/<sid>/chapters/<cid>")
@jwt_required()
@user_required
def user_specific_chapter(sid,cid):
    u = get_current_user()
    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid).scalar()

    if c is None:
        return jsonify(msg = "Chapter not found!"), 400
    
    if c.subject not in u.subjects:
        return jsonify(msg = "User not registered for subject!"),400

    return jsonify(payload=c.serialise(required = "quizes")),200