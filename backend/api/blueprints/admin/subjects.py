from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required
from sqlalchemy.exc import IntegrityError

admin_subject_routes = Blueprint('admin_subject_routes', __name__, url_prefix="/subjects")


@admin_subject_routes.get("/")
@jwt_required()
@admin_required
def all_subjects():
    """
        LIVE
        See all subjects.
        GET http://localhost:5000/admin/subjects/

        Query string args: page, per_page and q (for filtering)

        Expected on success: List of all subjects according to query.
    """
    
    page = int(request.args.get("page",1))
    per_page = int(request.args.get("per_page",5))
    q = request.args.get("q",None)

    if not q:
        query = Subject.query.filter().paginate(page=page,per_page=per_page,max_per_page=10)
    else:
        query = Subject.query.filter(Subject.name.startswith(q)).paginate(page=page,per_page=per_page,max_per_page=10)
    res = [s.serialise() for s in query]
    
    return jsonify(payload=res,pages=query.pages)

@admin_subject_routes.get("/<id>")
@jwt_required()
@admin_required
def specific_subjects(id):
    """
        LIVE
        See specific subject.
        GET http://localhost:5000/admin/subjects/:id

        Expected on success: Specific subject details with chapter information
    """
    s = Subject.query.filter(Subject.id == id).scalar()
    if s:
        return jsonify(payload=s.serialise(required=['chapters']))
    
    return jsonify(msg="No such subject found!"),400

@admin_subject_routes.post("/")
@jwt_required()
@admin_required
def add_subject():
    """
        Add new subject.
        POST http://localhost:5000/admin/subjects

        Request body: name,description,credits

        Expected on success: Creation of new Subject in db
    """
    name = request.form.get("name",None)
    description = request.form.get("description",None)
    credits = int(request.form.get("credits",0))

    if credits == 0 or name is None:
        return jsonify(msg="Malformed request: Check if all fields included"),400
    
    s = Subject(name = name, credits = credits, description = description)
    try:
        db.session.add(s)
        db.session.commit()
        return jsonify(msg="Subject creation successful"),200
    
    except IntegrityError as e:
        return jsonify(msg="Name is not unique!"),400
    



@admin_subject_routes.get("/<sid>/chapters")
@jwt_required()
@admin_required
def all_chapters(sid):
    """
        See chapters of a particular subject.
        GET http://localhost:5000/admin/subjects/:sid/chapters

        Expected on success: Subject details along with list of chapters
    """
    s = Subject.query.filter(Subject.id == sid).scalar()
    if s:
        return jsonify(payload = s.serialise(required=("chapters")))
    
    return jsonify(msg="Subject not found!"),400

@admin_subject_routes.get("/<sid>/chapters/<cid>")
@jwt_required()
@admin_required
def specific_chapter(sid,cid):
    """
        See particular chapter information.
        GET http://localhost:5000/admin/subjects/:sid/chapters/:cid

        Expected on success: Chapter details
    """
    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid).scalar()
    if c:
        return jsonify(payload = c.serialise())
    
    return jsonify(msg="Subject or chapter not found!"),400

@admin_subject_routes.post("/<sid>/chapters")
@jwt_required()
@admin_required
def add_chapter(sid):
    """
        Add chapter.
        POST http://localhost:5000/admin/subjects/:sid/chapters

        Request body: name, description

        Expected on success: Chapter creation
    """
    
    name = request.form.get("name",None)
    description = request.form.get("description",None)

    if name is None:
        return jsonify(msg="Malformed request!"),400
    
    s = Subject.query.filter(Subject.id == sid).scalar()
    if s is None:
        return jsonify(msg="Subject not found!"),400
    
    c = Chapter(name = name, description = description, subject_id = sid)
    db.session.add(c)
    db.session.commit()
    
    return jsonify(msg="Chapter created!"),200




@admin_subject_routes.get("/<sid>/chapters/<cid>/quizes")
@jwt_required()
@admin_required
def all_quizes(sid,cid):
    """
        See quizes of a particular chapter.
        GET http://localhost:5000/admin/subjects/:sid/chapters/:cid/quizes

        Expected on success: Chapter details along with list of quizes
    """

    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid).scalar()
    if c:
        return jsonify(payload = c.serialise(required=("quizes")))
    
    return jsonify(msg="Subject or chapter not found!"),400

@admin_subject_routes.get("/<sid>/chapters/<cid>/quizes/<qid>")
@jwt_required()
@admin_required
def specific_quiz(sid,cid,qid):
    """
        See specific quiz details.
        GET http://localhost:5000/admin/subjects/:sid/chapters/:cid/quizes/:qid

        Expected on success: Specific quiz details
    """
    q = Quiz.query.filter(Quiz.id == qid, Quiz.chapter_id == cid).scalar()

    if q and q.chapter.subject_id == sid:
        return jsonify(payload = q.serialise())
    
    return jsonify(msg="Subject, chapter or quiz not found!"),400

@admin_subject_routes.post("/<sid>/chapters/<cid>/quizes")
@jwt_required()
@admin_required
def add_quiz(sid,cid):
    """
        Add new quiz.
        POST http://localhost:5000/admin/subjects/:sid/chapters/:cid/quizes

        Request Body: dated, duration, description

        Expected on success: Quiz object created in db
    """

    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid).scalar()
    if c:
        dated = request.form.get("dated",None)
        duration = request.form.get("duration",None)
        description = request.form.get("description",None)

        if dated is None or duration is None:
            return jsonify(msg="Malformed request!"),400    

        q = Quiz(chapter_id = cid, dated = dated, duration = duration, description = description)
        return jsonify(msg="Quiz added!"),200
    
    return jsonify(msg="Subject or chapter not found!"),400




@admin_subject_routes.get("/<sid>/chapters/<cid>/questions")
@jwt_required()
@admin_required
def see_questions(sid,cid):
    """
        See all questions for a chapter.
        GET http://localhost:5000/admin/subjects/:sid/chapters/:cid/questions

        Expected on success: Chapter information with list of all questions
    """
    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid).scalar()
    if c:
        return jsonify(payload = c.serialise(required=("questions")))
    
    return jsonify(msg="Subject or chapter not found!"),400

@admin_subject_routes.get("/<sid>/chapters/<cid>/questions/<qid>")
@jwt_required()
@admin_required
def specific_question(sid,cid,qid):
    """
        See specific question.
        GET http://localhost:5000/admin/subjects/:sid/chapters/:cid/questions/:qid

        Expected on success: Question information
    """
    q = Question.query.filter(Question.id == qid, Question.chapter_id == cid).scalar()
    if q:
        if q.chapter.subject_id == sid:
            return jsonify(payload = q.serialise())
    
    return jsonify(msg="Subject, chapter or quiz not found!"),400

@admin_subject_routes.post("/<sid>/chapters/<cid>/questions")
@jwt_required()
@admin_required
def add_question(sid,cid):
    """
        Add new question.
        POST http://localhost:5000/admin/subjects/:sid/chapters/:cid/questions

        Expected on success: Question creation
    """
    
    description = request.form.get("description", None)
    correct = int(request.form.get("correct", -1))
    marks = request.form.get("marks",None)
    
    options = []
    for i in range(4):
        o = request.form.get(f"options[{i}]", None)
        if o is None:
            return jsonify(msg="Malformed request!"),400
        
        options.append(o)

    if description is None or correct == -1 or marks is None:
        return jsonify(msg="Malformed request!"),400

    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid)
    if c is None:
        return jsonify(msg="Subject or chapter not found!"),400
    
    q = Question(description=description,options="#".join(options),correct = correct, marks = marks, chapter_id = cid)
    db.session.add(q)
    db.session.commit()

    return jsonify(msg="Question created successfully!"),200


    
@admin_subject_routes.get("/<sid>/enrolled")
@jwt_required()
@admin_required
def see_enrolled(sid):
    """
        Add new question.
        POST http://localhost:5000/admin/subjects/:sid/enrolled

        Expected on success: Question creation
    """
    s = Subject.query.filter(Subject.id == sid).scalar()
    if s:
        return jsonify(payload=s.serialise(required=['users']))
    
    return jsonify(msg="No such subject found!"),400

  