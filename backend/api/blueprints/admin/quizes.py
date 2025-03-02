from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required
from datetime import datetime, timedelta

# Base URL: /admin/subjects/<sid>/chapters/<cid>/quizes
admin_quiz_routes = Blueprint('admin_quiz_routes', __name__)

@admin_quiz_routes.get("/")
@jwt_required()
@admin_required
def all_quizes(sid,cid):
    """
        LIVE, STABLE
        See quizes of a particular chapter.
        GET /admin/subjects/:sid/chapters/:cid/quizes

        Expected on success: Chapter information with paginated list of quizes per filter
        Expected to be handled by frontend:
            200 - Empty payload, frontend should render some message
            400 - Invalid filter passed
            404 - Subject/Chapter not found
    """

    # User input from query string
    filter_ = request.args.get("filter", "pending")

    if filter_ not in ["pending", "past", "all"]:
        return jsonify("Invalid filter passed!"), 400
    
    current_datetime = datetime.now()
    quizes = Quiz.query.filter(Quiz.chapter_id == int(cid)).all()

    payload = []
    if filter_ == "all":
        payload = [q.serialise() for q in Quiz.query.filter(Quiz.chapter_id == cid)]
        return jsonify(payload = payload), 200

    for q in quizes:
        if filter_ == "pending":
            # Has not ended - current time < end time of quiz
            if current_datetime < q.dated + timedelta(minutes = q.duration):
                payload.append(q.serialise())

        elif filter_ == "past":
            # Only quizes that have ended already
            if current_datetime > q.dated + timedelta(minutes = q.duration):
                payload.append(q.serialise())

        else:
            return jsonify("Invalid filter passed!"), 400
    
    return jsonify(payload = payload), 200

@admin_quiz_routes.put("/<qid>")
@jwt_required()
@admin_required
def edit_quiz(sid,cid,qid):
    """
        LIVE
        Edit specific quiz.
        PUT /admin/subjects/:sid/chapters/:cid/quizes/:qid

        Expected on success: Quiz information edited
        Expected to be handled by frontend:
            400 - Db errors
            400 - Validation errors
            404 - Subject/Chapter not found
    """

    # User input from form
    dated = request.form.get("dated",None)
    duration = request.form.get("duration",None)
    description = request.form.get("description",None)

    q = Quiz.query.filter(Quiz.id == qid, Quiz.chapter_id == cid).scalar()

    # Checking existence of quiz in given chapter and subject
    if q and q.chapter.subject_id == int(sid):
        if dated:
            # Do not touch - Specific date format
            quiz_date = datetime(
                year=int(dated[:4]),
                month=int(dated[5:7]),
                day=int(dated[8:10]),
                hour=int(dated[11:13]),
                minute=int(dated[14:16])
            )
            q.dated = quiz_date
        
        if duration:
            # Validation - duration - int > 0
            try:
                duration = int(duration)
                if duration > 0:
                    q.duration = duration
                else:
                    return jsonify(msg="Bad request: Duration must be non-zero and positive!"), 400

            except ValueError as e:
                return jsonify(msg="Bad request: Duration must be an integer!"), 400
                
        if description:
            q.description = description
        
        # Checking for db errors
        try:
            db.session.commit()

        except Exception as e:
            print(e)
            return jsonify(msg="Database error!"), 400
        
        return jsonify(msg="Quiz editing success!"),200
    
    return jsonify(msg="Subject, chapter or quiz not found!"),400


@admin_quiz_routes.get("/<qid>")
@jwt_required()
@admin_required
def specific_quiz(sid,cid,qid):
    """
        LIVE STABLE
        See specific quiz details.
        GET /admin/subjects/:sid/chapters/:cid/quizes/:qid

        Expected on success: Quiz information
        Expected to be handled by frontend:
            404 - Subject/Chapter not found
    """

    q = Quiz.query.filter(Quiz.id == qid, Quiz.chapter_id == cid).scalar()
    if q and q.chapter.subject_id == int(sid):
        return jsonify(payload = q.serialise())
    
    return jsonify(msg="Subject, chapter or quiz not found!"),400

@admin_quiz_routes.get("/<qid>/questions")
@jwt_required()
@admin_required
def specific_quiz_questions(sid,cid,qid):
    """
        LIVE
        See questions in quiz by filter.
        GET /admin/subjects/:sid/chapters/:cid/quizes/:qid

        Expected on success: Quiz question information filtered and paginated
        Expected to be handled by frontend:
            404 - Subject/Chapter not found
            400 - Invalid filter
    """

    # User input through query_string
    query_str = request.args.get("q","")
    filter_ = request.args.get("filter","all")
    
    q = Quiz.query.filter(Quiz.id == qid, Quiz.chapter_id == cid).scalar()

    if not (q and q.chapter.subject_id == int(sid)):
        return jsonify(msg="Subject, chapter or quiz not found!"),400

    if filter_ == "present":
        # All questions that are in quiz
        if len(query_str) == 0:
            return jsonify(payload=[x.serialise() for x in q.questions])
        
        # All questions that are in quiz starting with query_str
        else:
            return jsonify(payload=[x.serialise() for x in q.questions.filter(Question.description.contains(query_str))])

    elif filter_ == "absent":
         # All questions that are not in quiz
         if len(query_str) == 0:
            return jsonify(payload=[x.serialise() for x in Question.query.filter(Question.chapter_id == int(cid)).all() if x not in q.questions])
         
         # All questions that are not in quiz starting with query_str
         else:
            return jsonify(payload=[x.serialise() for x in Question.query.filter(Question.chapter_id == int(cid), Question.description.contains(query_str)).all() if x not in q.questions])
    
    elif filter_ == "all":
         # All questions in chapter
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
         
         # All questions in chapter with starting query_str
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
