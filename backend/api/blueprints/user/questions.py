from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required, get_current_user
from api.models import *
from api.blueprints.user import user_required
from datetime import datetime,timedelta

# Base URL: /user/subjects/<sid>/chapters/<cid>/quizes/<quiz_id>/questions/
user_question_routes = Blueprint('user_question_routes', __name__)

@user_question_routes.get("/<question_id>")
@jwt_required()
@user_required
def user_fetch_question_response(sid,cid,quiz_id,question_id):
    """
        Returns the response and the question on query
        GET /user/subjects/<sid>/chapters/<cid>/quizes/<quiz_id>/questions/<question_id>

        Expected on success: Returns the serialised question and serialised response for
        a particular question for a particular user. If quiz has not ended yet, question
        is sent in unsafe mode.
    """
    user = get_current_user()

    # Validation - existence
    quiz = Quiz.query.filter(Quiz.id == quiz_id).scalar()
    if quiz is None:
        return jsonify(msg = "Quiz not found!"), 404
    
    current_datetime = datetime.now()

    # Pending quiz
    if current_datetime < quiz.dated:
        return jsonify(msg = 'Cannot fetch question/response of pending quiz!'),400
    
    else:
        # Finding time left in quiz
        remaining_time = quiz.dated + timedelta(minutes = quiz.duration) - current_datetime
        seconds = int(remaining_time.total_seconds())

        query = quiz.questions
        num = query.count()
        question = [x for x in quiz.questions.offset(int(question_id) - 1).limit(1)][0]
        actual_question_id = question.id

        r = Response.query.filter(Response.user_id == user.id, Response.question_id == actual_question_id, Response.quiz_id == quiz_id).scalar()

        if current_datetime < quiz.dated + timedelta(minutes = quiz.duration):
            if r:
                return jsonify(payload = r.marked, question = question.serialise(required = ('unsafe')), num = num, time = seconds), 200
            return jsonify(payload = -1, question = question.serialise(required = ('unsafe')), num = num, time = seconds), 200

        if r:
            return jsonify(payload = r.marked, question = question.serialise(), num = num, time = seconds), 200
        return jsonify(payload = -1, question = question.serialise(), num = num, time = seconds), 200

@user_question_routes.post("/<question_id>")
@jwt_required()
@user_required
def user_answer_question(sid,cid,quiz_id,question_id):
    """
        STABLE - 25/03/2025
        Marks the user response to a particular quiz question.
        POST /user/subjects/<sid>/chapters/<cid>/quizes/<quiz_id>/questions/<question_id>

        Expected on success: Constructs/modifies response object to reflect user answer.
        Additional information: Should only work when quiz is active. If answer cleared
        then response object will get deleted!
    """
    user = get_current_user()
    marked = request.form.get("marked",-1)
    
    try:
        marked = int(marked)
    except ValueError:
        return jsonify(msg = "Invalid option selected!"), 400

    quiz = Quiz.query.filter(Quiz.id == quiz_id).scalar()
    if quiz is None:
        return jsonify(msg = "No such quiz found!"), 400
    
    actual_question_id = [x.id for x in quiz.questions.offset(int(question_id) - 1).limit(1)][0]
    current_datetime = datetime.now()

    if (current_datetime > quiz.dated + timedelta(minutes=quiz.duration)):
        return jsonify(msg = "Quiz attempt time expired!"), 400
    
    if (current_datetime < quiz.dated):
        return jsonify(msg = "Quiz has not started!"), 400

    r = Response.query.filter(Response.user_id == user.id, Response.question_id == actual_question_id, Response.quiz_id == quiz_id).scalar()
    # Answer cleared!
    if marked == -1:
        if r:
            db.session.delete(r)
            db.session.commit()
        return jsonify(msg = "Response deleted!"), 200

    elif 0 <= marked < 4:
        # Answer added!
        if r is None:
            r = Response(user_id = user.id, quiz_id = quiz_id, question_id = actual_question_id, marked = marked, answered_at = datetime.now())
            db.session.add(r)
            db.session.commit()
            return jsonify(msg = "Response created!"), 200

        # Answer modified!
        else:
            r.marked = marked
            r.answered_at = datetime.now()
            db.session.commit()
            return jsonify(msg = "Response modified!"), 200

    else:
        return jsonify(msg = "Invalid option selected!"),400