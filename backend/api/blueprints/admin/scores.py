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
    query_all = db.session.query(Response, Quiz, Question).join(Quiz, Quiz.id == Response.quiz_id).join(Question, Question.id == Response.question_id).filter(Quiz.id == qid, Response.user_id == uid)
    count_all = query_all.count()

    query_correct = query_all.filter(Response.marked == Question.correct)
    count_correct = query_correct.count()
    
    return jsonify(correct = count_correct, count = count_all),200

@admin_score_routes.get("/users/<uid>/subjects/<sid>/chapters/<cid>/quizes/<qid>/coverage")
@jwt_required()
@admin_required
def get_question_coverage_quiz(uid,sid,cid,qid):
    """
    Of all questions in quiz how many answered?
    """
    query_all = Quiz.query.filter(Quiz.id == qid).scalar().questions
    count_all = query_all.count()

    query_attempted = db.session.query(Response, Question, Quiz).join(Question, Question.id == Response.question_id).join(Quiz, Quiz.id == Response.quiz_id).filter(Quiz.id == qid, Response.user_id == uid)
    count_attempted = query_attempted.count()
    
    return jsonify(count = count_all, attempted = count_attempted),200
