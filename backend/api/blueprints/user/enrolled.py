from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required, get_current_user
from api.models import *
from api.blueprints.user import user_required
from sqlalchemy.exc import IntegrityError

# Base URL: /user/enrolled
user_enrolled_routes = Blueprint('user_enrolled_routes', __name__)

@user_enrolled_routes.post("/")
@jwt_required()
@user_required
def enroll_course():
    """
        STABLE - 25/03/2025
        Send request to enroll in subject
        POST /user/enrolled/

        Expected on success: Creation of new requested record.
    """
    user = get_current_user()
    sid = request.form.get("subject_id", None)

    if sid is None:
        return jsonify(msg = "Bad request: subject_id not included!"), 400

    s = Subject.query.filter(Subject.id == sid).scalar()
    # Validation - existence
    if s:
        # Validation - existence
        if s in user.subjects:
            return jsonify(msg = "User already enrolled!"), 200
        
        try:
            r = Requested(user_id = user.id, subject_id = sid)
            db.session.add(r)
            db.session.commit()
            return jsonify(msg = "User request sent!"), 200
        
        except IntegrityError as e:
            return jsonify(msg = "User request already exists!"), 200

    return jsonify(msg = "Subject not found!"), 400

@user_enrolled_routes.get("/")
@jwt_required()
@user_required
def requested_subjects():
    """
        STABLE - 25/03/2025
        View all requested subjects!
        GET /user/enrolled/

        Expected on success: Serialised list of all subjects requested (non-paginated!).
    """
    user = get_current_user()
    return jsonify(payload = [x.subject.serialise() for x in user.requested])