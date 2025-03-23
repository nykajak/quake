from flask import Blueprint,jsonify
from flask_jwt_extended import jwt_required, get_current_user
from api.models import *
from api.blueprints.user import user_required
from api import cache

user_subject_routes = Blueprint('user_subject_routes', __name__)


@user_subject_routes.get("/all")
@jwt_required()
@user_required
def available_subjects():
    """
        GET /user/subjects/all
    """
    u = get_current_user()
    # TO DO - Figure out a way to display all subjects user is allwoed to enroll for efficiently

    enrolled = [x.id for x in u.subjects]
    requested = [x.subject_id for x in db.session.query(Requested).filter(Requested.user_id == u.id)]
    subjects = [x.serialise() for x in db.session.query(Subject).filter(Subject.id.notin_(enrolled),Subject.id.notin_(requested))]
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
    # TO DO - Make users be able to access subject metadata (only) for all subjects

    u = get_current_user()
    @cache.memoize(10)
    def fetch_subject(sid,u):
        s = Subject.query.filter(Subject.id == sid).scalar()

        if s is None:
            return jsonify(msg = "Subject not found!"), 400
        
        if s not in u.subjects:
            return jsonify(msg = "User not registered for subject!"),400

        return jsonify(payload=s.serialise('chapters')),200

    return fetch_subject(sid,u)