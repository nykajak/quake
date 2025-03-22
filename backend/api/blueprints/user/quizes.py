from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required,get_current_user
from api.models import *
from api.blueprints.user import user_required
from api.blueprints.pagination import pagination_validation

user_quiz_routes = Blueprint('user_quiz_routes', __name__)

@user_quiz_routes.get("/<qid>/questions")
@jwt_required()
@user_required
def user_questions(sid,cid,qid):
    """
    
    """
    page = request.args.get("page",1)
    per_page = request.args.get("per_page",5)
    
    return_val,validation = pagination_validation(page,per_page)
    if validation != 200:
        return validation
    
    page, per_page = return_val
    MAX_QUESTIONS_PER_PAGE = 10

    user = get_current_user()
    quiz = Quiz.query.filter(Quiz.id == qid).scalar()
    if quiz is None:
        return jsonify(msg = "No such quiz found!"), 400
    
    current_datetime = datetime.datetime.now()

    
    if (current_datetime < quiz.dated):
        return jsonify(msg = "Quiz has not started!"), 400
    
    if (current_datetime < quiz.dated + datetime.timedelta(minutes=quiz.duration)):
        return jsonify(payload = [{"question":x.serialise(required=("unsafe"))} for x in quiz.questions], quiz = quiz.serialise())

    payload = []
    query = quiz.questions.paginate(page = page, per_page = per_page, max_per_page = MAX_QUESTIONS_PER_PAGE)
    for question in query:
        temp_dict = {}

        response = question.responses.filter(Response.user_id == user.id,Response.quiz_id == quiz.id).all()
        if len(response):
            temp_dict = response[0].serialise()
        else:
            temp_dict = {"marked": -1}
        temp_dict["question"] = question.serialise()

        payload.append(temp_dict)

    return jsonify(payload = payload, quiz = quiz.serialise(), pages = query.pages)


@user_quiz_routes.get("/<qid>")
@jwt_required()
@user_required
def user_quiz_view(sid,cid,qid):
    user = get_current_user()
    quiz = Quiz.query.filter(Quiz.id == qid).scalar()
    if quiz is None:
        return jsonify(msg = "No such quiz found!"), 400
    
    current_datetime = datetime.datetime.now()

    if (current_datetime > quiz.dated + datetime.timedelta(minutes=quiz.duration)):
        # Quiz expired
        score = Score.query.filter(Score.user_id == user.id, Score.quiz_id == qid).scalar()
        if score:
            return jsonify(correct_count = score.correct_count, response_count = score.attempted_count, question_count = score.question_count),200

        response_count_query = db.session.query(Response)
        response_count_query = response_count_query.join(Response.question).join(Response.quiz).join(Response.user)
        response_count_query = response_count_query.filter(Quiz.id == qid, User.id == user.id)
        response_count = response_count_query.count()

        correct_count_query = response_count_query.filter(Response.marked == Question.correct)
        correct_count = correct_count_query.count()

        question_count = quiz.questions.count()

        score = Score(user_id = user.id, quiz_id = qid, attempted_count = response_count, question_count = question_count, correct_count = correct_count)
        db.session.add(score)
        db.session.commit()

        return jsonify(payload=quiz.serialise(),active = False, correct_count = correct_count, response_count = response_count, question_count = question_count), 200
    
    elif (current_datetime < quiz.dated):
        # Quiz yet to start
        return jsonify(payload=quiz.serialise(),active=False), 200
    
    else:
        # Quiz is active and live
        return jsonify(payload=quiz.serialise(),active=True), 200
