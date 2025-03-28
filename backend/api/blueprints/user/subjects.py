from flask import Blueprint,jsonify, request
from flask_jwt_extended import jwt_required, get_current_user
from api.models import *
from api.blueprints.user import user_required
from api import cache
from api.blueprints.pagination import pagination_validation

# Base URL: /user/subjects
user_subject_routes = Blueprint('user_subject_routes', __name__)

@cache.memoize(10)
def query_specific_subject(uid, sid):
    s = db.session.query(Subject).join(Subject.users)
    s = s.filter(Subject.id == sid, User.id == uid).scalar()
    if s is not None:
        return s.serialise('chapters')
    return s

@user_subject_routes.get("/all")
@jwt_required()
@user_required
def available_subjects():
    """
        Returns the list of subjects that user can enroll for
        GET /user/subjects/all

        Expected on success: Returns the serialised list of subjects
        that a user can enroll for.
    """
    u = get_current_user()

    # Already enrolled!
    enrolled = [x.id for x in u.subjects]

    # Already requested!
    requested = [x.subject_id for x in db.session.query(Requested).filter(Requested.user_id == u.id)]

    subjects = [x.serialise() for x in db.session.query(Subject).filter(Subject.id.notin_(enrolled),Subject.id.notin_(requested))]
    return jsonify(payload=subjects),200

@user_subject_routes.get("/")
@jwt_required()
@user_required
def user_subjects():
    """
        Returns the list of subjects that user is enrolled for
        GET /user/subjects/

        Expected on success: Returns the serialised, paginated list of subjects
        that a user is enrolled in.
    """

    page = request.args.get("page",1)
    per_page = request.args.get("per_page",5)
    query_string = request.args.get("q", None)

    return_val,validation = pagination_validation(page,per_page)
    if validation != 200:
        return validation
    
    page, per_page = return_val

    u = get_current_user()

    if query_string is None:
        subjects = u.subjects.paginate(page = page, per_page = per_page, max_per_page = 10)
    else:
        subjects = u.subjects.filter(Subject.name.startswith(query_string))
        subjects = subjects.paginate(page = page, per_page = per_page, max_per_page = 10)

    u = u.serialise()
    u["subjects"] = [x.serialise() for x in subjects]
    return jsonify(payload=u, pages = subjects.pages),200
    


@user_subject_routes.get("/<sid>")
@jwt_required()
@user_required
def user_specific_subject(sid):
    """
        Returns specific subject details
        GET /user/subjects/:sid

        Expected on success: Returns the serialised subject details (plus chapter)
    """
    
    u = get_current_user()
    s = query_specific_subject(u.id, sid)
    if s is None:
        return jsonify(msg = "Subject not found!"), 400

    return jsonify(payload=s),200