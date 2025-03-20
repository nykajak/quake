from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required

# Base URL: /admin/scores
admin_score_routes = Blueprint('admin_score_routes', __name__)


@admin_score_routes.get("/users/<uid>/subjects/<sid>")
@jwt_required()
@admin_required
def get_score_summary_subject(uid,sid):

    # Fetch no of questions in subject
    question_count_query = db.session.query(Question, Chapter, Subject)
    question_count_query = question_count_query.join(Chapter, Chapter.id == Question.chapter_id).join(Subject, Subject.id == Chapter.subject_id)
    question_count = question_count_query.count()

    # Fetch no of responses by user in subject
    response_count_query = db.session.query(Response, Question, Chapter, Subject)
    response_count_query = response_count_query.join(Question, Question.id == Response.question_id).join(Chapter, Chapter.id == Question.chapter_id).join(Subject, Subject.id == Chapter.subject_id)
    response_count_query = response_count_query.filter(Subject.id == sid,Response.user_id == uid)
    response_count = response_count_query.count()

    # Compute no of questions seen by user in subject
    questions_seen = set()
    for r,q,c,s in response_count_query:
        questions_seen.add(q.id)

    questions_seen_count = len(questions_seen)

    # Fetch no of correct responses by user in subject
    response_correct_query = response_count_query.filter(Response.marked == Question.correct)
    correct_count = response_correct_query.count()

    return jsonify(correct_count = correct_count, response_count = response_count, question_count = question_count, seen_count = questions_seen_count), 200

@admin_score_routes.get("/users/<uid>/subjects/<sid>/chapters/<cid>")
@jwt_required()
@admin_required
def get_score_summary_chapter(uid,sid,cid):
    
    # Fetch no of questions in subject
    question_count_query = db.session.query(Question, Chapter)
    question_count_query = question_count_query.join(Chapter, Chapter.id == Question.chapter_id)
    question_count = question_count_query.count()

    # Fetch no of responses by user in subject
    response_count_query = db.session.query(Response, Question, Chapter)
    response_count_query = response_count_query.join(Question, Question.id == Response.question_id).join(Chapter, Chapter.id == Question.chapter_id)
    response_count_query = response_count_query.filter(Chapter.id == cid,Response.user_id == uid)
    response_count = response_count_query.count()

    # Compute no of questions seen by user in subject
    questions_seen = set()
    for r,q,c in response_count_query:
        questions_seen.add(q.id)

    questions_seen_count = len(questions_seen)

    # Fetch no of correct responses by user in subject
    response_correct_query = response_count_query.filter(Response.marked == Question.correct)
    correct_count = response_correct_query.count()
    
    return jsonify(correct_count = correct_count, response_count = response_count, question_count = question_count, seen_count = questions_seen_count), 200

@admin_score_routes.get("/users/<uid>/subjects/<sid>/chapters/<cid>/quizes/<qid>")
@jwt_required()
@admin_required
def get_score_summary_quiz(uid,sid,cid,qid):

    score = Score.query.filter(Score.user_id == uid, Score.quiz_id == qid).scalar()
    if score:
        return jsonify(correct_count = score.correct_count, response_count = score.attempted_count, question_count = score.question_count),200

    # Fetch no of questions in a quiz
    question_count_query = Quiz.query.filter(Quiz.id == qid).scalar().questions
    question_count = question_count_query.count()

    # Fetch no of responses for a quiz by some user
    response_count_query = db.session.query(Response, Quiz, Question)
    response_count_query = response_count_query.join(Quiz, Quiz.id == Response.quiz_id).join(Question, Question.id == Response.question_id)
    response_count_query = response_count_query.filter(Quiz.id == qid, Response.user_id == uid)
    response_count = response_count_query.count()

    # Fetch no of correct responses
    response_correct_query = response_count_query.filter(Response.marked == Question.correct)
    correct_count = response_correct_query.count()

    score = Score(user_id = uid, quiz_id = qid, attempted_count = response_count, question_count = question_count, correct_count = correct_count)
    db.session.add(score)
    db.session.commit()
    
    return jsonify(correct_count = correct_count, response_count = response_count, question_count = question_count),200
