from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required

# Base URL: /admin/subjects/<sid>/chapters/<cid>/questions
admin_question_routes = Blueprint('admin_question_routes', __name__)

@admin_question_routes.get("/")
@jwt_required()
@admin_required
def see_questions(sid,cid):
    """
        LIVE
        See questions for some chapter.
        GET /admin/subjects/:sid/chapters/:cid/questions

        Expected on success: Chapter information with paginated list of all questions
        Expected to be handled by frontend:
            200 - Empty payload, frontend should render some message
            404 - Subject/Chapter not found
    """

    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid).scalar()
    if c:
        return jsonify(payload = c.serialise(required=("questions"))), 200
    
    return jsonify(msg="Subject or chapter not found!"), 400

@admin_question_routes.put("/<qid>")
@jwt_required()
@admin_required
def edit_question(sid,cid,qid):
    """
        LIVE, STABLE
        Edit specific question.
        PUT /admin/subjects/:sid/chapters/:cid/questions/:qid

        Expected on success: Question information updated.
        Expected to be handled by frontend:
            400 - Validation error!
            400 - Database error!
            404 - Subject/Chapter/Quiz not found
    """

    # User data through form
    description = request.form.get("description",None)
    correct = request.form.get("correct",None)
    marks = request.form.get("marks",None)

    # options[0], options[1], options[2], options[3] are options A,B,C,D respectively
    options = [request.form.get(f"options[{i}]",None) for i in range(0,4)]

    q = Question.query.filter(Question.id == qid, Question.chapter_id == cid).scalar()
    if q:
        # Checking if question in correct subject
        if int(q.chapter.subject_id) == int(sid):

            # Validation - Question description must be non empty
            if description and len(description) > 0:
                q.description = description
            
            if marks:
                # Validation - marks should be integral > 0 
                try:
                    if int(marks) > 0:
                        q.marks = marks
                
                except ValueError as e:
                    return jsonify(msg = "Bad request: Marks should be integral and greater than 0!"), 400

            if correct:
                # Validation - correct should be integral x, 0 <= x <= 3
                try:
                    if 0 <= int(correct) <= 3:
                        q.correct = int(correct)
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
        LIVE, STABLE
        See specific question.
        GET /admin/subjects/:sid/chapters/:cid/questions/:qid

        Expected on success: Question information retrieved.
        Expected to be handled by frontend:
            404 - Subject/Chapter/Quiz not found
    """

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
        LIVE, STABLE
        Add new question.
        POST /admin/subjects/:sid/chapters/:cid/questions

        Expected on success: Question creation in backend. Return of question_id to frontend as payload
        Expected to be handled by frontend:
            404 - Subject/Chapter/Quiz not found
    """
    
    # User input through form
    description = request.form.get("description", None)
    correct = request.form.get("correct", -1)
    marks = request.form.get("marks", 1)
    
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
        q = Question(description=description,options="#".join(options),correct = correct, marks = marks, chapter_id = cid)
        db.session.add(q)
        db.session.commit()

    except Exception as e:
        print(e)
        return jsonify(msg ="Database error"), 400

    return jsonify(msg="Question created successfully!", payload = q.id), 200
