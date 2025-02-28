from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required, get_current_user
from api.models import *
from api.blueprints.user import user_required

user_question_routes = Blueprint('user_question_routes', __name__)


@user_question_routes.get("/<question_id>")
@jwt_required()
@user_required
def user_fetch_response(sid,cid,quiz_id,question_id):
    user = get_current_user()

    r = Response.query.filter(Response.user_id == user.id, Response.question_id == question_id, Response.quiz_id == quiz_id).scalar()
    if r:
        return jsonify(payload = r.marked), 200
    return jsonify(payload = -1), 200

@user_question_routes.post("/<question_id>")
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