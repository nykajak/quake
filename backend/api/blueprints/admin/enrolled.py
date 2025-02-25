from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required

admin_enrolled_routes = Blueprint('admin_enrolled_routes', __name__)

@admin_enrolled_routes.get("/")
@jwt_required()
@admin_required
def see_enrolled(sid):
    """
        LIVE
        See all students enrolled for subject.
        POST /admin/subjects/:sid/enrolled

        Expected on success: List of users enrolled for subject
    """
    s = Subject.query.filter(Subject.id == sid).scalar()
    if s:
        return jsonify(payload=s.serialise(required=['users']))
    
    return jsonify(msg="No such subject found!"),400
