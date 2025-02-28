from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required

admin_response_routes = Blueprint('admin_response_routes', __name__)


@admin_response_routes.get("/")
@jwt_required()
@admin_required
def admin_view_responses():
    user_id = request.args.get("user_id", None)
    quiz_id = request.args.get("quiz_id", None)
    question_id = request.args.get("question_id", None)

    r = Response.query
    params = ['user','quiz','question']

    if user_id is not None:
        r = r.filter(Response.user_id == user_id)
        del params[0]

    if quiz_id is not None:
        r = r.filter(Response.quiz_id == quiz_id)
        del params[1]

    if question_id is not None:
        r = r.filter(Response.question_id == question_id)
        del params[2]

    l = [x.serialise(required = params) for x in r]
    print(len(l))
    return jsonify(payload = l), 200