from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required

# Base URL: /admin/scores
admin_score_routes = Blueprint('admin_score_routes', __name__)

def recompute_score_all(qid):
    """
        Recomputes all scores of all users for quiz with id qid.
        Additional information: Deletion of scores to be done before call!
    """
    query_users = db.session.query(User)
    query_users = query_users.join(User.subjects).join(Subject.chapters).join(Chapter.quizes)
    query_users = query_users.filter(User.is_admin == 0)

    question_count_query = Quiz.query.filter(Quiz.id == qid).scalar().questions
    question_count = question_count_query.count()
    
    for user in query_users:
        attempted_count, correct_count = recompute_score_one(qid, user.id)
        score = Score(user_id = user.id, quiz_id = qid, attempted_count = attempted_count, question_count = question_count, correct_count = correct_count)
        db.session.add(score)

    db.session.commit()

def recompute_score_one(qid, uid):
    """
        Recomputes the score of a user for quiz with id qid.
    """

    # Fetch no of responses for a quiz by some user
    response_count_query = db.session.query(Response)
    response_count_query = response_count_query.join(Response.quiz).join(Response.question)
    response_count_query = response_count_query.filter(Quiz.id == qid, Response.user_id == uid)
    attempted_count = response_count_query.count()

    # Fetch no of correct responses
    response_correct_query = response_count_query.filter(Response.marked == Question.correct)
    correct_count = response_correct_query.count()

    return attempted_count, correct_count

@admin_score_routes.get("/users/<uid>/subjects/<sid>")
@jwt_required()
@admin_required
def get_score_summary_subject(uid,sid):
    """
        Return statistics of a particular user for a particular subject.
        GET /admin/scores/users/:uid/subjects/:sid
        
        Expected on success: correct_count, question_count, seen_count, response_count
        
        Addional information: correct_count - no of correct responses by this user,
        response_count - no of responses by this user, question_count - no of questions
        in this subject, seen_count - no of unique questions attempted by user in subject
    """

    # Fetch no of questions in subject
    question_count_query = db.session.query(Question)
    question_count_query = question_count_query.join(Question.chapter).join(Chapter.subject)
    question_count = question_count_query.count()

    # Fetch no of responses by user in subject
    response_count_query = db.session.query(Response)
    response_count_query = response_count_query.join(Response.question).join(Question.chapter).join(Chapter.subject)
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
    """
        Return statistics of a particular user for a particular chapter.
        GET /admin/scores/users/:uid/subjects/:sid/chapters/:cid
        
        Expected on success: correct_count, question_count, seen_count, response_count
        
        Addional information: correct_count - no of correct responses by this user,
        response_count - no of responses by this user, question_count - no of questions
        in this chapter, seen_count - no of unique questions attempted by user in chapter
    """

    # Fetch no of questions in chapter
    question_count_query = db.session.query(Question)
    question_count_query = question_count_query.join(Question.chapter).join(Chapter.subject)
    question_count = question_count_query.count()

    # Fetch no of responses by user in chapter
    response_count_query = db.session.query(Response)
    response_count_query = response_count_query.join(Response.question).join(Question.chapter).join(Chapter.subject)
    response_count_query = response_count_query.filter(Subject.id == sid, Chapter.id == cid, Response.user_id == uid)
    response_count = response_count_query.count()

    # Compute no of questions seen by user in chapter
    questions_seen = set()
    for r,q,c in response_count_query:
        questions_seen.add(q.id)

    questions_seen_count = len(questions_seen)

    # Fetch no of correct responses by user in chapter
    response_correct_query = response_count_query.filter(Response.marked == Question.correct)
    correct_count = response_correct_query.count()
    
    return jsonify(correct_count = correct_count, response_count = response_count, question_count = question_count, seen_count = questions_seen_count), 200

@admin_score_routes.get("/users/<uid>/subjects/<sid>/chapters/<cid>/quizes/<qid>")
@jwt_required()
@admin_required
def get_score_summary_quiz(uid,sid,cid,qid):
    """
        Return statistics of a particular user for a particular quiz.
        GET /admin/scores/users/:uid/subjects/:sid/chapters/:cid/quizes/:qid
        
        Expected on success: correct_count, question_count, response_count
        
        Addional information: correct_count - no of correct responses by this user in 
        quiz, response_count - no of responses by this user in quiz, question_count - 
        no of questions in this quiz.
    """

    # Check for existence of Score object!
    score = Score.query.filter(Score.user_id == uid, Score.quiz_id == qid).scalar()
    if score:
        return jsonify(correct_count = score.correct_count, response_count = score.attempted_count, question_count = score.question_count),200

    # Fetch no of questions in a quiz
    question_count_query = Quiz.query.filter(Quiz.id == qid).scalar().questions
    question_count = question_count_query.count()

    # Fetch other statistics!
    attempted_count, correct_count = recompute_score_one(qid,uid)

    # Construct a Score object
    score = Score(user_id = uid, quiz_id = qid, attempted_count = attempted_count, question_count = question_count, correct_count = correct_count)
    db.session.add(score)
    db.session.commit()
    
    return jsonify(correct_count = correct_count, response_count = attempted_count, question_count = question_count),200
