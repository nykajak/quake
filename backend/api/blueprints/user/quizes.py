from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.user import user_required

user_quiz_routes = Blueprint('user_quiz_routes', __name__)

@user_quiz_routes.get("/<qid>")
@jwt_required()
@user_required
def user_questions(sid,cid,qid):
    # TO DO - results could be paginated?
    quiz = Quiz.query.filter(Quiz.id == qid).scalar()
    if quiz is None:
        return jsonify(msg = "No such quiz found!"), 400
    
    current_datetime = datetime.datetime.now()

    if (current_datetime > quiz.dated + datetime.timedelta(minutes=quiz.duration)):
        return jsonify(msg = "Quiz attempt time expired!"), 400
    
    if (current_datetime < quiz.dated):
        return jsonify(msg = "Quiz has not started!"), 400
    
    quiz = Quiz.query.filter(Quiz.id == qid).scalar()
    remaining_time = quiz.dated + datetime.timedelta(minutes = quiz.duration) - datetime.datetime.now()
    
    seconds = int(remaining_time.total_seconds())
    return jsonify(payload = [x.serialise(required=("unsafe")) for x in quiz.questions], quiz = quiz.serialise(), time = seconds)
