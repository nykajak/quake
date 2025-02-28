from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required,get_current_user
from api.models import *
from api.blueprints.user import user_required

user_chapter_routes = Blueprint('user_chapter_routes', __name__)

@user_chapter_routes.get("/<cid>")
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