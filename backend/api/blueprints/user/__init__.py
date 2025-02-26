from functools import wraps
from flask import jsonify, Blueprint, request
from flask_jwt_extended import get_current_user, jwt_required
import datetime
from api.models import *

user_routes = Blueprint('user_routes', __name__)

# Add relevant documentation
# Add relevant error handling and graceful fail states

def user_required(fun):
    @wraps(fun)
    def inner(*args,**kwargs):
        current_user = get_current_user()
        if current_user.is_admin == 0:
            return fun(*args,**kwargs)
        return jsonify(msg="Not a user!"),400
    return inner

@user_routes.get("/")
@jwt_required()
@user_required
def profile():
    u = get_current_user()
    return jsonify(payload=u.serialise()),200

@user_routes.get("/subjects")
@jwt_required()
@user_required
def user_subjects():
    u = get_current_user()
    return jsonify(payload=u.serialise('subjects')),200

@user_routes.get("/subjects/<sid>")
@jwt_required()
@user_required
def user_specific_subject(sid):
    u = get_current_user()
    s = Subject.query.filter(Subject.id == sid).scalar()

    if s is None:
        return jsonify(msg = "Subject not found!"), 400
    
    if s not in u.subjects:
        return jsonify(msg = "User not registered for subject!"),400

    return jsonify(payload=s.serialise('chapters')),200

@user_routes.get("/subjects/<sid>/chapters/<cid>")
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

@user_routes.get("/subjects/<sid>/chapters/<cid>/quizes/<qid>")
@jwt_required()
@user_required
def user_questions(sid,cid,qid):
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
    print(remaining_time)
    questions = quiz.questions
    return jsonify(payload = [x.serialise(required=("unsafe")) for x in questions], quiz = quiz.serialise(), time = str(remaining_time))

@user_routes.get("/subjects/<sid>/chapters/<cid>/quizes/<quiz_id>/questions/<question_id>")
@jwt_required()
@user_required
def user_fetch_response(sid,cid,quiz_id,question_id):
    user = get_current_user()

    r = Response.query.filter(Response.user_id == user.id, Response.question_id == question_id, Response.quiz_id == quiz_id).scalar()
    if r:
        return jsonify(payload = r.marked), 200
    return jsonify(payload = -1), 200

@user_routes.post("/subjects/<sid>/chapters/<cid>/quizes/<quiz_id>/questions/<question_id>")
@jwt_required()
@user_required
def user_answer_question(sid,cid,quiz_id,question_id):
    user = get_current_user()
    marked = request.form.get("marked",-1)
    
    try:
        marked = int(marked)
    except ValueError:
        return jsonify(msg = "Invalid option selected!"), 400

    quiz = Quiz.query.filter(Quiz.id == quiz_id).scalar()
    if quiz is None:
        return jsonify(msg = "No such quiz found!"), 400
    
    current_datetime = datetime.datetime.now()

    if (current_datetime > quiz.dated + datetime.timedelta(minutes=quiz.duration)):
        return jsonify(msg = "Quiz attempt time expired!"), 400
    
    if (current_datetime < quiz.dated):
        return jsonify(msg = "Quiz has not started!"), 400

    r = Response.query.filter(Response.user_id == user.id, Response.question_id == question_id, Response.quiz_id == quiz_id).scalar()
    if marked == -1:
        if r:
            db.session.delete(r)
            db.session.commit()
        return jsonify(msg = "Response deleted!"), 200

    elif 0 <= marked < 4:
        if r is None:
            r = Response(user_id = user.id, quiz_id = quiz_id, question_id = question_id, marked = marked, answered_at = datetime.datetime.now())
            db.session.add(r)
            db.session.commit()
            return jsonify(msg = "Response created!"), 200

        else:
            r.marked = marked
            r.answered_at = datetime.datetime.now()
            db.session.commit()
            return jsonify(msg = "Response modified!"), 200

    else:
        return jsonify(msg = "Invalid option selected!"),400

@user_routes.post("/enroll")
@jwt_required()
@user_required
def enroll_course():
    user = get_current_user()
    sid = request.form.get("subject_id", None)

    if sid is None:
        return jsonify(msg = "Bad request: subject_id not included!"), 400

    s = Subject.query.filter(Subject.id == sid).scalar()
    if s:
        if s in user.subjects:
            return jsonify(msg = "User already enrolled!"), 200
        
        user.subjects.add(s)
        db.session.commit()
        return jsonify(msg = "User enrolled in course!"), 200

    return jsonify(msg = "Subject not found!"), 400