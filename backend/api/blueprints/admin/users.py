from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required
from sqlalchemy.exc import IntegrityError

admin_user_routes = Blueprint('admin_user_routes', __name__, url_prefix="/users")

@admin_user_routes.get("/")
@jwt_required()
@admin_required
def all_users():
    page = int(request.args.get("page",1))
    per_page = int(request.args.get("per_page",5))

    query = User.query.filter().paginate(page=page,per_page=per_page,max_per_page=10)
    res = [u.serialise() for u in query]
    
    return jsonify(payload=res)

@admin_user_routes.get("/<id>")
@jwt_required()
@admin_required
def specific_users(id):
    u = User.query.filter(User.id == id).scalar()
    if u:
        return jsonify(payload=u.serialise())
    return jsonify(msg="No such user found!"),400

@admin_user_routes.get("/<id>/subjects")
@jwt_required()
@admin_required
def specific_users_subjects(id):
    u = User.query.filter(User.id == id).scalar()
    if u:
        return jsonify(payload=u.serialise(required = ("subjects")))
    return jsonify(msg="No such user found!"),400

@admin_user_routes.post("/<uid>/subjects/<sid>")
@jwt_required()
@admin_required
def add_user_to_subject(uid,sid):
    u = User.query.filter(User.id == uid).scalar()
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
    u = User.query.filter(User.id == uid).scalar()
    s = Subject.query.filter(Subject.id == sid).scalar()
    if u and s:
        try:
            u.subjects.remove(s)
            db.session.commit()
            return jsonify(msg="Subject removed from user enrollment!"),200

        except ValueError as e:
            return jsonify(msg="User is not enrolled!"),400
    return jsonify(msg="No such user or subject found!"),400


@admin_user_routes.get("/<id>/scores")
@jwt_required()
@admin_required
def specific_users_scores(id):
    u = User.query.filter(User.id == id).scalar()
    if u:
        return jsonify(payload=u.serialise(required = ("scores")))
    return jsonify(msg="No such user found!"),400

@admin_user_routes.get("/<id>/responses")
@jwt_required()
@admin_required
def specific_users_responses(id):
    u = User.query.filter(User.id == id).scalar()
    if u:
        return jsonify(payload=u.serialise(required = ("responses")))
    return jsonify(msg="No such user found!"),400