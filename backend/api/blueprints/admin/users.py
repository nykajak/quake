from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError

admin_user_routes = Blueprint('admin_user_routes', __name__, url_prefix="/users")

# Error handling and graceful fail states

@admin_user_routes.get("/")
@jwt_required()
@admin_required
def all_users():
    """
        LIVE
        See all users.
        GET /admin/users/

        Query string args: page, per_page and q (for filtering)

        Expected on success: List of all users according to query.
    """
    page = int(request.args.get("page",1))
    per_page = int(request.args.get("per_page",5))
    q = request.args.get("q",None)

    if not q:
        query = User.query.filter(User.is_admin == 0).paginate(page=page,per_page=per_page,max_per_page=10)
    else:
        query = User.query.filter(User.is_admin == 0, User.name.startswith(q)).paginate(page=page,per_page=per_page,max_per_page=10)
    res = [u.serialise() for u in query]
    
    return jsonify(payload=res,pages=query.pages)

@admin_user_routes.get("/<id>")
@jwt_required()
@admin_required
def specific_users(id):
    """
        LIVE
        See specific user.
        GET /admin/users/:id

        Expected on success: Specific user details with subject information
    """
    u = User.query.filter(User.id == id, User.is_admin == 0).scalar()
    if u:
        return jsonify(payload=u.serialise(required=['subjects']))
    return jsonify(msg="No such user found!"),400




@admin_user_routes.post("/<uid>/subjects/<sid>")
@jwt_required()
@admin_required
def add_user_to_subject(uid,sid):
    """
        LIVE
        Enroll user in subject.
        POST /admin/users/:id/subjects/:sid

        Expected on success: User gains access to subject
    """
    u = User.query.filter(User.id == uid, User.is_admin == 0).scalar()
    s = Subject.query.filter(Subject.id == sid).scalar()
    if u and s:
        try:
            u.subjects.append(s)
            db.session.commit()
            return jsonify(msg = "Added subject!"),200
        except IntegrityError as e:
            return jsonify(msg = "Already enrolled!"),400
        
    return jsonify(msg="No such user or subject found!"),400

@admin_user_routes.delete("/<uid>/subjects/<sid>")
@jwt_required()
@admin_required
def remove_user_from_subject(uid,sid):
    """
        LIVE
        Un-enroll user in subject.
        DELETE /admin/users/:id/subjects/:sid

        Expected on success: User loses access to subject
    """
    u = User.query.filter(User.id == uid, User.is_admin == 0).scalar()
    s = Subject.query.filter(Subject.id == sid).scalar()
    if u and s:
        try:
            u.subjects.remove(s)
            db.session.commit()
            return jsonify(msg="Subject removed from user enrollment!"),200

        except StaleDataError as e:
            return jsonify(msg="User is not enrolled!"),400
    return jsonify(msg="No such user or subject found!"),400




@admin_user_routes.get("/<id>/scores")
@jwt_required()
@admin_required
def specific_users_scores(id):
    """
        Retreive user scores.
        GET /admin/users/:id/scores

        Expected on success: Summary of user scores
    """
    u = User.query.filter(User.id == id).scalar()
    if u:
        return jsonify(payload=u.serialise(required = ("scores")))
    return jsonify(msg="No such user found!"),400




@admin_user_routes.get("/<id>/responses")
@jwt_required()
@admin_required
def specific_users_responses(id):
    """
        Retreive user responses.
        GET /admin/users/:id/responses

        Expected on success: User details and list of user responses
    """
    u = User.query.filter(User.id == id).scalar()
    if u:
        return jsonify(payload=u.serialise(required = ("responses")))
    return jsonify(msg="No such user found!"),400