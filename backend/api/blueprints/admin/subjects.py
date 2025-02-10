from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required
from sqlalchemy.exc import IntegrityError

from datetime import datetime

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
def specific_subject(id):
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

@admin_subject_routes.put("/<id>")
@jwt_required()
@admin_required
def edit_subject(id):
    name = request.form.get("name", None)
    description = request.form.get("description", None)
    credits = request.form.get("credits", None)

    s = Subject.query.filter(Subject.id == id).scalar()
    if s:
        try:
            if name and len(name) > 0:
                s.name = name
            
            if description:
                s.description = description

            if credits:
                try:
                    credits = int(credits)
                    s.credits = credits
                except Exception as e:
                    print(type(e))
                    pass
            
            db.session.commit()

        except Exception as e:
            print(type(e))
            return jsonify(msg="Edit subject failure"),400

        return jsonify(msg="Edit subject success"),200
    
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
    
    credits = request.form.get("credits",0)
    try:
        credits = int(credits)
    except:
        return jsonify(msg="Malformed request: Check if all fields included"),400

    if credits == 0 or name is None:
        return jsonify(msg="Malformed request: Check if all fields included"),400
    
    s = Subject(name = name, credits = credits, description = description)
    try:
        db.session.add(s)
        db.session.commit()
        return jsonify(msg="Subject creation successful",payload=s.serialise()),200
    
    except IntegrityError as e:
        return jsonify(msg="Name is not unique!"),400
    

@admin_subject_routes.get("/<sid>/chapters/<cid>")
@jwt_required()
@admin_required
def specific_chapter(sid,cid):
    """
        LIVE
        See particular chapter information.
        GET http://localhost:5000/admin/subjects/:sid/chapters/:cid

        Expected on success: Chapter details
    """
    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid).scalar()
    if c:
        return jsonify(payload = c.serialise())
    
    return jsonify(msg="Subject or chapter not found!"),400

@admin_subject_routes.put("/<sid>/chapters/<cid>")
@jwt_required()
@admin_required
def edit_chapter(sid,cid):
    name = request.form.get("name",None)
    description = request.form.get("description",None)

    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid).scalar()
    if c:
        if name and len(name) > 0:
            c.name = name

        if description:
            c.description = description
        
        db.session.commit()
        return jsonify(msg="Chapter edit success!"),200

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
    
    return jsonify(msg="Chapter created!",payload=c.serialise()),200




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

@admin_subject_routes.put("/<sid>/chapters/<cid>/quizes/<qid>")
@jwt_required()
@admin_required
def edit_quiz(sid,cid,qid):
    dated = request.form.get("dated",None)
    duration = request.form.get("duration",None)
    description = request.form.get("description",None)

    q = Quiz.query.filter(Quiz.id == qid, Quiz.chapter_id == cid).scalar()

    if q and q.chapter.subject_id == int(sid):
        if dated:
            x = datetime(year=int(dated[:4]),month=int(dated[5:7]),day=int(dated[8:10]),hour=int(dated[11:13]),minute=int(dated[14:16]))
            q.dated = x
        
        if duration:
            try:
                q.duration = int(duration)

            except Exception as e:
                print(type(e))
                pass

        if description:
            q.description = description

        db.session.commit()
        return jsonify(msg="Quiz editing success!"),200
    
    return jsonify(msg="Subject, chapter or quiz not found!"),400


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

    if q and q.chapter.subject_id == int(sid):
        return jsonify(payload = q.serialise())
    
    return jsonify(msg="Subject, chapter or quiz not found!"),400

@admin_subject_routes.get("/<sid>/chapters/<cid>/quizes/<qid>/questions")
@jwt_required()
@admin_required
def specific_quiz_questions(sid,cid,qid):
    query_str = request.args.get("q","")
    filter = request.args.get("filter","none")
    
    q = Quiz.query.filter(Quiz.id == qid, Quiz.chapter_id == cid).scalar()

    if not (q and q.chapter.subject_id == int(sid)):
        return jsonify(msg="Subject, chapter or quiz not found!"),400

    if filter == "present":
        if len(query_str) == 0:
            return jsonify(payload=[x.serialise() for x in q.questions])
        
        else:
            return jsonify(payload=[x.serialise() for x in q.questions.filter(Question.description.contains(query_str))])

    elif filter == "absent":
         if len(query_str) == 0:
            return jsonify(payload=[x.serialise() for x in Question.query.filter(Question.chapter_id == int(cid)).all() if x not in q.questions])
         
         else:
            return jsonify(payload=[x.serialise() for x in Question.query.filter(Question.chapter_id == int(cid), Question.description.contains(query_str)).all() if x not in q.questions])
    
    elif filter == "none":
         if len(query_str) == 0:
            return jsonify(payload=[x.serialise() for x in Question.query.filter(Question.chapter_id == int(cid)).all()])
         
         else:
            return jsonify(payload=[x.serialise() for x in Question.query.filter(Question.chapter_id == int(cid), Question.description.contains(query_str)).all()])
    
    else:
        return jsonify(msg="Invalid filter provided!"),400

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

        x = datetime(year=int(dated[:4]),month=int(dated[5:7]),day=int(dated[8:10]),hour=int(dated[11:13]),minute=int(dated[14:16]))
        q = Quiz(chapter_id = cid, dated = x, duration = int(duration), description = description)
        db.session.add(q)
        db.session.commit()
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

@admin_subject_routes.put("/<sid>/chapters/<cid>/questions/<qid>")
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
        if int(q.chapter.subject_id) == int(sid):
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
        LIVE
        See all students enrolled for subject.
        POST http://localhost:5000/admin/subjects/:sid/enrolled

        Expected on success: List of users enrolled for subject
    """
    s = Subject.query.filter(Subject.id == sid).scalar()
    if s:
        return jsonify(payload=s.serialise(required=['users']))
    
    return jsonify(msg="No such subject found!"),400

  