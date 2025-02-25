from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required
from datetime import datetime, timedelta

admin_quiz_routes = Blueprint('admin_quiz_routes', __name__)

@admin_quiz_routes.get("/")
@jwt_required()
@admin_required
def all_quizes(sid,cid):
    """
        See quizes of a particular chapter.
        GET /admin/subjects/:sid/chapters/:cid/quizes

        Expected on success: Chapter details along with list of quizes
    """

    filter_ = request.args.get("filter", "pending")

    if filter_ not in ["pending", "past"]:
        return jsonify("Invalid filter passed!"), 400
    
    current_datetime = datetime.now()
    quizes = Quiz.query.filter(Quiz.chapter_id == int(cid)).all()

    new_ = []
    for q in quizes:
        if filter_ == "pending":
            if current_datetime < q.dated + timedelta(minutes = q.duration):
                new_.append(q.serialise())

        else:
            if current_datetime > q.dated + timedelta(minutes = q.duration):
                new_.append(q.serialise())
    
    return jsonify(payload = new_),200

@admin_quiz_routes.put("/<qid>")
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


@admin_quiz_routes.get("/<qid>")
@jwt_required()
@admin_required
def specific_quiz(sid,cid,qid):
    """
        See specific quiz details.
        GET /admin/subjects/:sid/chapters/:cid/quizes/:qid

        Expected on success: Specific quiz details
    """
    q = Quiz.query.filter(Quiz.id == qid, Quiz.chapter_id == cid).scalar()

    if q and q.chapter.subject_id == int(sid):
        return jsonify(payload = q.serialise())
    
    return jsonify(msg="Subject, chapter or quiz not found!"),400

@admin_quiz_routes.get("/<qid>/questions")
@jwt_required()
@admin_required
def specific_quiz_questions(sid,cid,qid):
    query_str = request.args.get("q","")
    filter = request.args.get("filter","all")
    
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
    
    elif filter == "all":
         if len(query_str) == 0:
            l = []
            for x in Question.query.filter(Question.chapter_id == int(cid)).all():
                obj = x.serialise()
                if x in q.questions:
                    obj["present"] = True
                else:
                    obj["present"] = False
                l.append(obj)

            return jsonify(payload=l)
         
         else:
            l = []
            for x in Question.query.filter(Question.chapter_id == int(cid), Question.description.contains(query_str)).all():
                obj = x.serialise()
                if x in q.questions:
                    obj["present"] = True
                else:
                    obj["present"] = False
                l.append(obj)

            return jsonify(payload=l)
    
    else:
        return jsonify(msg="Invalid filter provided!"),400
    
@admin_quiz_routes.post("/<qid>/questions/add")
@jwt_required()
@admin_required
def add_question_to_quiz(sid,cid,qid):
    question_id = request.form.get("question_id",None)

    if question_id is None:
        return jsonify(msg="Malformed request!"),400
    
    try:
        question_id = int(question_id)
    except ValueError as e:
        return jsonify(msg="Malformed request!"),400

    question = Question.query.filter(Question.id == question_id).scalar()
    quiz = Quiz.query.filter(Quiz.id == qid).scalar()

    if question.chapter.id != quiz.chapter.id:
        return jsonify(msg="Cannot add question from different chapter!"),400

    quiz.questions.append(question)
    db.session.commit()
    return jsonify(msg="Question successfully added!"),200

@admin_quiz_routes.post("/<qid>/questions/remove")
@jwt_required()
@admin_required
def remove_question_from_quiz(sid,cid,qid):
    question_id = request.form.get("question_id",None)
    print(request.data)

    if question_id is None:
        return jsonify(msg="Malformed request!"),400
    
    try:
        question_id = int(question_id)
    except ValueError as e:
        return jsonify(msg="Malformed request!"),400

    question = Question.query.filter(Question.id == question_id).scalar()
    quiz = Quiz.query.filter(Quiz.id == qid).scalar()

    if question.chapter.id != quiz.chapter.id:
        return jsonify(msg="Cannot perform operation on question from different chapter!"),400

    quiz.questions.remove(question)
    db.session.commit()
    return jsonify(msg="Question successfully removed!"),200

@admin_quiz_routes.post("/")
@jwt_required()
@admin_required
def add_quiz(sid,cid):
    """
        Add new quiz.
        POST /admin/subjects/:sid/chapters/:cid/quizes

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
