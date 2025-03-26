from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required
from api.blueprints.pagination import pagination_validation
from datetime import datetime
from api.blueprints.admin.scores import get_score_summary_quiz,recompute_score_all

# Base URL: /admin/subjects/<sid>/chapters/<cid>/questions
admin_question_routes = Blueprint('admin_question_routes', __name__)

@admin_question_routes.get("/")
@jwt_required()
@admin_required
def see_questions(sid,cid):
    """
        See questions that are part of some chapter.
        GET /admin/subjects/:sid/chapters/:cid/questions

        Expected on success: Paginated serialised payload {"questions":questions}
    """

    # Note: Change response to payload = questions[]
    page = request.args.get("page", 1)
    per_page = request.args.get("per_page", 5)

    return_val,validation = pagination_validation(page,per_page)
    if validation != 200:
        return validation
    
    page, per_page = return_val

    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid).scalar()
    if c:
        MAX_QUESTIONS_PER_PAGE = 10
        query = c.questions.paginate(page = page, per_page = per_page, max_per_page = MAX_QUESTIONS_PER_PAGE)
        questions = [x.serialise() for x in query]
        return jsonify(payload = {"questions":questions}, pages = query.pages), 200
    
    return jsonify(msg="Subject or chapter not found!"), 400

@admin_question_routes.put("/<qid>")
@jwt_required()
@admin_required
def edit_question(sid,cid,qid):
    """
        Edit specific question.
        PUT /admin/subjects/:sid/chapters/:cid/questions/:qid

        Expected on success: Question information updated.
        Additional information: Edit can partially succeed silently. (If valid)
        Currently questions that are part of older quizes will still be edited,
        making the score computed obsolete.
    """
    # Note: Need to add recomputation for scores for previous quizes when updating
    # correct or prevent editing for questions that have already been added to quizes

    # User data through form
    description = request.form.get("description",None)
    correct = request.form.get("correct",None)

    # options[0], options[1], options[2], options[3] are options A,B,C,D respectively
    options = [request.form.get(f"options[{i}]",None) for i in range(0,4)]

    q = Question.query.filter(Question.id == qid, Question.chapter_id == cid).scalar()
    if q:
        # Checking if question in correct subject
        if int(q.chapter.subject_id) == int(sid):

            # Validation - Question description must be non empty
            if description and len(description) > 0:
                q.description = description
        
            if correct:
                # Validation - correct should be integral x, 0 <= x <= 3
                try:
                    if 0 <= int(correct) <= 3:
                        prev_value = q.correct
                        q.correct = int(correct)

                        if prev_value != int(correct):
                            # Force score deletion for each user
                            quiz_ids = [quiz.id for quiz in q.quizes]
                            query = Score.query.filter(Score.quiz_id.in_(quiz_ids))
                            query = query.delete()

                            # Force score recomputation for each user
                            for quiz_id in quiz_ids:
                                recompute_score_all(quiz_id)

                    else:
                        return jsonify(msg = "Bad request: Correct should be value between 0-3 (inclusive)!"), 400
                
                except ValueError as e:
                    return jsonify(msg = "Bad request: Correct should be integral!"), 400
            
            x = q.options.split("#")

            for i in range(4):
                # Validation - options should be non empty
                if options[i] and len(options[i]) > 0:
                    x[i] = options[i]

            q.options = "#".join(x)

            try:
                db.session.commit()

            except Exception as e:
                print(e)
                return jsonify(msg="Database error!"), 400

            return jsonify(msg="Question edit success"), 200

    return jsonify(msg="Subject, chapter or quiz not found!"),400

@admin_question_routes.get("/<qid>")
@jwt_required()
@admin_required
def specific_question(sid,cid,qid):
    """
        See specific question.
        GET /admin/subjects/:sid/chapters/:cid/questions/:qid

        Expected on success: Question information retrieved as payload.
    """
    # Note: Perhaps replace with db.session.query with join? Avoids ambiguity!
    q = Question.query.filter(Question.id == qid, Question.chapter_id == cid).scalar()
    if q:
        if int(q.chapter.subject_id) == int(sid):
            return jsonify(payload = q.serialise())
    
    return jsonify(msg="Subject, chapter or quiz not found!"),400

@admin_question_routes.post("/")
@jwt_required()
@admin_required
def add_question(sid,cid):
    """
        STABLE - 24/03/2025
        Add new question.
        POST /admin/subjects/:sid/chapters/:cid/questions

        Expected on success: Question creation in backend. Question_id as payload
    """
    
    # User input through form
    description = request.form.get("description", None)
    correct = request.form.get("correct", -1)
    
    options = []
    for i in range(4):
        # Validation - options[i] must be non-empty
        option = request.form.get(f"options[{i}]", None) # option[i] is ith options 0 <= i <= 3
        if option is None or len(option) <= 0:
            return jsonify(msg = f"Malformed request! Option {1 + i} missing"), 400
        
        options.append(option)

    # Validation - correct must be integral
    try:
        correct = int(correct)
    
    except ValueError as e:
        return jsonify(msg = f"Malformed request! correct should be integral"), 400

    # Validation - description must be non empty
    if description is None or len(description) <= 0:
        return jsonify(msg="Malformed request! description should be non empty"),400
    
    # Validation - correct must be in [0,3]
    if correct > 3 or correct < 0:
        return jsonify(msg = f"Malformed request! correct should be within [0,3]"), 400

    # Validation - chapter and subject must exist
    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid)
    if c is None:
        return jsonify(msg="Subject or chapter not found!"),400
    
    # Checking for db errors
    try:
        q = Question(description=description,options="#".join(options),correct = correct, chapter_id = cid)
        db.session.add(q)
        db.session.commit()

    except Exception as e:
        print(e)
        return jsonify(msg ="Database error"), 400

    return jsonify(msg="Question created successfully!", payload = q.id), 200

@admin_question_routes.delete("/<qid>")
@jwt_required()
@admin_required
def admin_delete_question(sid,cid,qid):
    """
        Delete specific question.
        DELETE /admin/subjects/:sid/chapters/:cid/questions/:qid

        Expected on success: Question deletion from backend.
        Additional information: Question being deleted causes all quizes to lose that
        as a question, subsequently requiring recalculation of scores for past quizes
        where it was a member. The quizes themselves aren't deleted.
    """
    question = Question.query.filter(Question.id == qid).scalar()
    quiz_ids = [x.id for x in question.quizes.filter(Quiz.dated < datetime.now())]

    if question is None:
        return jsonify(msg = "No such question found!"), 404
    
    try:
        # Delete cascade, as given in models.py
        db.session.delete(question)
        db.session.commit()

    except Exception as e:
        print(e)
        return jsonify("Question deletion failed!"), 400

    # Force score deletion for each user
    query = Score.query.filter(Score.quiz_id.in_(quiz_ids))
    query = query.delete()

    # Force score recomputation for each user
    for quiz_id in quiz_ids:
        recompute_score_all(quiz_id)
        
    return jsonify("Question deletion success!"), 200