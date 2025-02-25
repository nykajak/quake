from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required

admin_question_routes = Blueprint('admin_question_routes', __name__)

@admin_question_routes.get("/")
@jwt_required()
@admin_required
def see_questions(sid,cid):
    """
        See all questions for a chapter.
        GET /admin/subjects/:sid/chapters/:cid/questions

        Expected on success: Chapter information with list of all questions
    """
    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid).scalar()
    if c:
        return jsonify(payload = c.serialise(required=("questions")))
    
    return jsonify(msg="Subject or chapter not found!"),400

@admin_question_routes.put("/<qid>")
@jwt_required()
@admin_required
def edit_question(sid,cid,qid):
    description = request.form.get("description",None)
    correct = request.form.get("correct",None)
    marks = request.form.get("marks",None)
    options = [request.form.get(f"options[{i}]",None) for i in range(0,4)]

    q = Question.query.filter(Question.id == qid, Question.chapter_id == cid).scalar()

    if q:
        if int(q.chapter.subject_id) == int(sid):
            if description and len(description) > 0:
                q.description = description
            
            if marks:
                try:
                    if int(marks) > 0:
                        q.marks = marks
                
                except Exception as e:
                    print(type(e))
                    pass

            if correct:
                try:
                    if 0 <= int(correct) <= 3:
                        q.correct = int(correct)
                
                except Exception as e:
                    print(type(e))
                    pass
            
            x = q.options.split("#")

            for i in range(4):
                if options[i] and len(options[i]) > 0:
                    x[i] = options[i]

            q.options = "#".join(x)

            db.session.commit()

            return jsonify(msg="Question edit success")
    
    return jsonify(msg="Subject, chapter or quiz not found!"),400

@admin_question_routes.get("/<qid>")
@jwt_required()
@admin_required
def specific_question(sid,cid,qid):
    """
        See specific question.
        GET /admin/subjects/:sid/chapters/:cid/questions/:qid

        Expected on success: Question information
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
        Add new question.
        POST /admin/subjects/:sid/chapters/:cid/questions

        Expected on success: Question creation
    """
    
    description = request.form.get("description", None)
    correct = int(request.form.get("correct", -1))
    marks = request.form.get("marks", 1)
    
    options = []
    for i in range(4):
        o = request.form.get(f"options[{i}]", None)
        if o is None:
            return jsonify(msg="Malformed request!"),400
        
        options.append(o)

    if description is None or correct == -1:
        return jsonify(msg="Malformed request!"),400

    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid)
    if c is None:
        return jsonify(msg="Subject or chapter not found!"),400
    
    q = Question(description=description,options="#".join(options),correct = correct, marks = marks, chapter_id = cid)
    db.session.add(q)
    db.session.commit()

    return jsonify(msg="Question created successfully!", payload = q.id),200
