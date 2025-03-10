from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required,get_current_user
from api.models import *
from api.blueprints.user import user_required

user_response_routes = Blueprint('user_response_routes', __name__)

@user_response_routes.get("/quizes/<qid>")
@jwt_required()
@user_required
def user_responses_for_quiz(qid):
    user = get_current_user()

    # TO DO - Pagination of results
    r = [x.serialise(required = ('question')) for x in Response.query.filter(Response.user_id == user.id, Response.quiz_id == qid)]
    return jsonify(payload=r),200

@user_response_routes.get("/quizes/<quiz_id>/questions/<question_id>")
@jwt_required()
@user_required
def user_response_for_question(quiz_id, question_id):
    user = get_current_user()

    # TO DO - Pagination of results
    r = Response.query.filter(Response.user_id == user.id, Response.quiz_id == quiz_id, Response.question_id == question_id).scalar()
    if r:
        return jsonify(payload=r.serialise(required=('question'))),200
    
    q = Question.query.filter(Question.id == question_id).scalar()
    if not q:
        return jsonify(msg = "No such question found!"), 404

    return jsonify(payload = {"question": q.serialise(), "marked": -1}),200