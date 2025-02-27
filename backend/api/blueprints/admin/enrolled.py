from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError

admin_enrolled_routes = Blueprint('admin_enrolled_routes', __name__)

@admin_enrolled_routes.get("/requests")
@jwt_required()
@admin_required
def see_requests():
    """
        See all pending requests for enrollment.
        GET /admin/enrolled/requests

        Expected on success: Return payload of all pending requests.
    """

    l = db.session.query(Requested, User, Subject).join(User,  Requested.user_id == User.id).join(Subject,  Requested.subject_id == Subject.id)
    l = [{"user":x[1].serialise(),"subject":x[2].serialise()} for x in l]

    return jsonify(payload = l), 200

@admin_enrolled_routes.get("/subjects/<sid>")
@jwt_required()
@admin_required
def see_enrolled(sid):
    """
        LIVE
        See all students enrolled for subject.
        POST /admin/enrolled/subjects/:sid

        Expected on success: List of users enrolled for subject
    """
    s = Subject.query.filter(Subject.id == sid).scalar()
    if s:
        return jsonify(payload=s.serialise(required=['users']))
    
    return jsonify(msg="No such subject found!"),400


@admin_enrolled_routes.post("users/<uid>/subjects/<sid>")
@jwt_required()
@admin_required
def add_user_to_subject(uid,sid):
    """
        LIVE
        Enroll user in subject.
        POST /admin/enrolled/users/:id/subjects/:sid

        Expected on success: User gains access to subject
        Expected to be handled by frontend:
            Frontend should not be able to change request sent.
    """
    u = User.query.filter(User.id == uid, User.is_admin == 0).scalar()
    s = Subject.query.filter(Subject.id == sid).scalar()
    if u and s:
        try:
            u.subjects.append(s)
            db.session.commit()
            return jsonify(msg = "Added subject!"),200
        except IntegrityError as e:
            return jsonify(msg = "Already enrolled!"),200
        
    return jsonify(msg="No such user or subject found!"),400

@admin_enrolled_routes.delete("/users/<uid>/subjects/<sid>")
@jwt_required()
@admin_required
def remove_user_from_subject(uid,sid):
    """
        LIVE
        Un-enroll user in subject.
        DELETE /admin/enrolled/users/:id/subjects/:sid

        Expected on success: User loses access to subject
        Expected to be handled by frontend:
            Frontend should not be able to change request sent.
    """
    u = User.query.filter(User.id == uid, User.is_admin == 0).scalar()
    s = Subject.query.filter(Subject.id == sid).scalar()
    if u and s:
        try:
            u.subjects.remove(s)
            db.session.commit()
            return jsonify(msg="Subject removed from user enrollment!"),200

        except StaleDataError as e:
            return jsonify(msg="User is not enrolled!"),200
    return jsonify(msg="No such user or subject found!"),400

