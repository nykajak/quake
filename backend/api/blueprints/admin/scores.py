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
    """
        How many correct responses among all responses?
    """
    query_all = db.session.query(Response, Question, Chapter, Subject).join(Question, Question.id == Response.question_id).join(Chapter, Chapter.id == Question.chapter_id).join(Subject, Subject.id == Chapter.subject_id).filter(Subject.id == sid,Response.user_id == uid)
    count_all = query_all.count()

    query_correct = query_all.filter(Response.marked == Question.correct)
    count_correct = query_correct.count()
    
    return jsonify(correct = count_correct, count = count_all),200

@admin_score_routes.get("/users/<uid>/subjects/<sid>/chapters/<cid>")
@jwt_required()
@admin_required
def get_score_summary_chapter(uid,sid,cid):
    """
        How many correct responses among all responses?
    """
    query_all = db.session.query(Response, Question, Chapter).join(Question, Question.id == Response.question_id).join(Chapter, Chapter.id == Question.chapter_id).filter(Chapter.id == cid,Response.user_id == uid)
    count_all = query_all.count()

    query_correct = query_all.filter(Response.marked == Question.correct)
    count_correct = query_correct.count()
    
    return jsonify(correct = count_correct, count = count_all),200

@admin_score_routes.get("/users/<uid>/subjects/<sid>/coverage")
@jwt_required()
@admin_required
def get_question_coverage_subject(uid,sid):
    """
        How many questions attempted among all questions?
    """
    query_all = db.session.query(Question, Chapter, Subject).join(Chapter, Chapter.id == Question.chapter_id).join(Subject, Subject.id == Chapter.subject_id).filter(Subject.id == sid)
    count_all = query_all.count()
    
    query_attempted = db.session.query(Response, Question, Chapter, Subject).join(Question, Question.id == Response.question_id).join(Chapter, Chapter.id == Question.chapter_id).join(Subject, Subject.id == Chapter.subject_id).filter(Subject.id == sid, Response.user_id == uid)
    count_attempted = query_attempted.count()
    
    return jsonify(count = count_all, attempted = count_attempted),200


@admin_score_routes.get("/users/<uid>/subjects/<sid>/chapters/<cid>/coverage")
@jwt_required()
@admin_required
def get_question_coverage_chapter(uid,sid,cid):
    """
        How many questions attempted among all questions?
    """
    query_all = db.session.query(Question, Chapter).join(Chapter, Chapter.id == Question.chapter_id).filter(Chapter.id == cid)
    count_all = query_all.count()

    query_attempted = db.session.query(Response, Question, Chapter).join(Question, Question.id == Response.question_id).join(Chapter, Chapter.id == Question.chapter_id).filter(Chapter.id == cid, Response.user_id == uid)
    count_attempted = query_attempted.count()
    
    return jsonify(count = count_all, attempted = count_attempted),200


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
