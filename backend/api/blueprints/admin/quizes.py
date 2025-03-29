from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required
from datetime import datetime, timedelta
from sqlalchemy.orm.exc import StaleDataError
from sqlalchemy import func
from api.blueprints.pagination import pagination_validation
from api import cache

# Base URL: /admin/subjects/<sid>/chapters/<cid>/quizes
admin_quiz_routes = Blueprint('admin_quiz_routes', __name__)

@admin_quiz_routes.get("/")
@jwt_required()
@admin_required
def all_quizes(sid,cid):
    """
        STABLE - 24/03/2025
        See quizes of a particular chapter.
        GET /admin/subjects/:sid/chapters/:cid/quizes

        Expected on success: Payload - paginated list of quizes after applying filter
        Additional information: Quizes split into two categories - past and pending
    """

    # User input from query string
    filter_ = request.args.get("filter", "pending")
    page = request.args.get("page",1)
    per_page = request.args.get("per_page",5)

    return_val,validation = pagination_validation(page,per_page)
    if validation != 200:
        return validation
    
    page, per_page = return_val

    MAX_QUIZES_PER_PAGE = 10

    if filter_ not in ["pending", "past", "all"]:
        return jsonify("Invalid filter passed!"), 400
    
    current_datetime = datetime.now()
    quizes = Quiz.query.filter(Quiz.chapter_id == int(cid))

    # Here pending refers to all quizes which have yet to start and past
    # refers to all quizes that have already started
    
    if filter_ == "pending":
        # Has not ended - start time > current
        quizes = quizes.filter(Quiz.dated > current_datetime)
    elif filter_ == "past":
        # Only quizes that have ended already - start time < current 
        quizes = quizes.filter(Quiz.dated < current_datetime)
    else:
        return jsonify("Invalid filter passed!"), 400
    
    quizes = quizes.paginate(page = page, per_page=per_page, max_per_page = MAX_QUIZES_PER_PAGE)
    return jsonify(payload = [x.serialise() for x in quizes], pages = quizes.pages), 200

@admin_quiz_routes.put("/<qid>")
@jwt_required()
@admin_required
def edit_quiz(sid,cid,qid):
    """
        Edit specific quiz.
        PUT /admin/subjects/:sid/chapters/:cid/quizes/:qid

        Expected on success: Quiz information edited (if valid)
        Additional information: Quizes handled differently based on past/pending.
        Fields - duration and dated of past quizes cannot be changed!
    """

    # User input from form
    dated = request.form.get("dated",None)
    duration = request.form.get("duration",None)
    description = request.form.get("description",None)

    q = Quiz.query.filter(Quiz.id == qid, Quiz.chapter_id == cid).scalar()
    current_date = datetime.now()

    # Checking existence of quiz in given chapter and subject
    if q and q.chapter.subject_id == int(sid):
        cache.delete_memoized(specific_quiz, sid, cid, qid)
        if dated:
            # Changes to dated cannot be made once quiz has ended
            if current_date < q.dated + timedelta(minutes = q.duration):
                # Do not touch - Specific date format
                quiz_date = datetime(
                    year=int(dated[:4]),
                    month=int(dated[5:7]),
                    day=int(dated[8:10]),
                    hour=int(dated[11:13]),
                    minute=int(dated[14:16])
                )
                q.dated = quiz_date

            else:
                return jsonify(msg = 'Cannot change date of a past quiz'),400
        
        if duration:
            # Validation - duration - int > 0
            try:
                duration = int(duration)

            except ValueError as e:
                return jsonify(msg="Bad request: Duration must be an integer!"), 400
            
            # Changes to duration cannot be made once quiz has ended
            if current_date < q.dated + timedelta(minutes = q.duration):
                if duration > 0:
                    q.duration = duration
                
                else:
                    return jsonify(msg="Bad request: Duration must be non-zero and positive!"), 400
            else:
                return jsonify(msg = 'Cannot change duration of a past quiz'),400
        
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
@cache.memoize(10)
def specific_quiz(sid,cid,qid):
    """
        See specific quiz details.
        GET /admin/subjects/:sid/chapters/:cid/quizes/:qid

        Expected on success: Serialised quiz information. (only)
    """
    q = db.session.query(Quiz)
    q = q.join(Quiz.chapter).join(Chapter.subject)
    q = q.filter(Quiz.id == qid, Chapter.id == cid, Subject.id == sid).scalar()
    if q:
        return jsonify(payload = q.serialise())
    
    return jsonify(msg="Subject, chapter or quiz not found!"),400

@admin_quiz_routes.get("/<qid>/questions")
@jwt_required()
@admin_required
def specific_quiz_questions(sid,cid,qid):
    """
        See questions in quiz by filter.
        GET /admin/subjects/:sid/chapters/:cid/quizes/:qid

        Expected on success: Quiz question information filtered and paginated
    """

    # User input through query_string
    query_str = request.args.get("q","")
    filter_ = request.args.get("filter","present")

    page = request.args.get("page",1)
    per_page = request.args.get("per_page",5)

    return_val,validation = pagination_validation(page,per_page)
    if validation != 200:
        return validation
    
    page, per_page = return_val
    MAX_QUESTIONS_PER_PAGE = 10
    
    q = db.session.query(Quiz)
    q = q.join(Quiz.chapter).join(Chapter.subject)
    q = q.filter(Quiz.id == qid, Chapter.id == cid, Subject.id == sid).scalar()

    if not (q and q.chapter.subject_id == int(sid)):
        return jsonify(msg="Subject, chapter or quiz not found!"),400

    if filter_ == "present":
        # All questions that are in quiz
        
        query = q.questions
        if len(query_str) != 0:
            query = query.filter(Question.description.contains(query_str))
        
        query = query.paginate(page = page, per_page = per_page, max_per_page = MAX_QUESTIONS_PER_PAGE)
        return jsonify(payload=[x.serialise() for x in query], pages = query.pages)

    elif filter_ == "absent":
        # All questions that are not in quiz
        query = Question.query.filter(Question.chapter_id == int(cid), Question.id.not_in([x.id for x in q.questions]))
        if len(query_str) != 0:
            query = query.filter(Question.description.contains(query_str))

        query = query.paginate(page = page, per_page = per_page, max_per_page = MAX_QUESTIONS_PER_PAGE)
        return jsonify(payload=[x.serialise() for x in query], pages = query.pages)
    
    elif filter_ == "all":
        # All questions in chapter
        query = Question.query.filter(Question.chapter_id == int(cid))
        if len(query_str) != 0:
            query = query.filter(Question.description.contains(query_str))

        query = query.paginate(page = page, per_page = per_page, max_per_page = MAX_QUESTIONS_PER_PAGE)
        l = []
        for x in query:
            obj = x.serialise()
            if x in q.questions:
                obj["present"] = True
            else:
                obj["present"] = False
            l.append(obj)

        return jsonify(payload=l, pages = query.pages)
    
    else:
        return jsonify(msg="Invalid filter provided!"),400
    
@admin_quiz_routes.post("/<qid>/questions/add")
@jwt_required()
@admin_required
def add_question_to_quiz(sid,cid,qid):
    """
        STABLE - 24/03/2025
        Add question to quiz.
        POST /admin/subjects/:sid/chapters/:cid/quizes/:qid/questions/add

        Expected on success: Question added to quiz in backend via problem.
        Additional information: Past quizes cannot have questions added!
    """
    question_id = request.form.get("question_id",None)

    if question_id is None:
        return jsonify(msg="Malformed request!"),400

    # Validation - Can only add questions before end of quiz
    current_time = datetime.now()
    quiz = Quiz.query.filter(Quiz.id == qid).scalar()
    if quiz.dated + timedelta(minutes=quiz.duration) < current_time:
        return jsonify(msg="Unable to add questions to a past quiz!"), 400
    
    question = Question.query.filter(Question.id == question_id).scalar()

    # Validation - Existence
    if question is None or quiz is None:
        return jsonify(msg="Quiz or question not found!"),404

    # Validation - Must be same chapter
    if question.chapter.id != quiz.chapter.id:
        return jsonify(msg="Cannot add question from different chapter!"),400

    quiz.questions.append(question)
    db.session.commit()
    return jsonify(msg="Question successfully added!"),200

@admin_quiz_routes.post("/<qid>/questions/remove")
@jwt_required()
@admin_required
def remove_question_from_quiz(sid,cid,qid):
    """
        STABLE - 24/03/2025
        Remove question from quiz.
        POST /admin/subjects/:sid/chapters/:cid/quizes/:qid/questions/remove

        Expected on success: Question removed from quiz in backend via problem.
        Additional information: Past quizes cannot have questions removed unless
        question is deleted!
    """
    question_id = request.form.get("question_id",None)

    # Validation - Can only remove questions before end of quiz
    current_time = datetime.now()
    if quiz.dated < current_time:
        return jsonify(msg="Unable to remove questions from a past quiz!"), 400

    question = Question.query.filter(Question.id == question_id).scalar()
    quiz = Quiz.query.filter(Quiz.id == qid).scalar()

    # Validation - Existence
    if question is None or quiz is None:
        return jsonify(msg="Quiz or question not found!"),404

    # Validation - Chapters must match
    if question.chapter.id != quiz.chapter.id:
        return jsonify(msg="Cannot perform operation on question from different chapter!"),400
    
    try: 
        quiz.questions.remove(question)
        db.session.commit()
        return jsonify(msg="Question successfully removed!"),200

    except StaleDataError as e:
        return jsonify(msg = "Question was never added!"), 200


@admin_quiz_routes.post("/")
@jwt_required()
@admin_required
def add_quiz(sid,cid):
    """
        STABLE - 24/03/2025
        Add new quiz.
        POST /admin/subjects/:sid/chapters/:cid/quizes

        Expected on success: Quiz object added to db.
        Additionak information: Quiz validation for dates is strict - No backdated
        quizes.
    """

    # Form data
    dated = request.form.get("dated",None)
    duration = request.form.get("duration",None)
    description = request.form.get("description",None)

    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid).scalar()

    # Validation - Existence
    if c:
        if dated is None or duration is None:
            return jsonify(msg="Malformed request!"),400    

        x = datetime(year=int(dated[:4]),month=int(dated[5:7]),day=int(dated[8:10]),hour=int(dated[11:13]),minute=int(dated[14:16]))
        current_time = datetime.now()

        # Validation - Quiz dated cannot be in the past!
        if x < current_time:
            return jsonify(msg="Cannot create quiz in the past!"),400

        q = Quiz(chapter_id = cid, dated = x, duration = int(duration), description = description)
        db.session.add(q)
        db.session.commit()
        return jsonify(msg="Quiz added!", payload = q.id),200
    
    return jsonify(msg="Subject or chapter not found!"),400

@admin_quiz_routes.delete("/<qid>")
@jwt_required()
@admin_required
def admin_quiz_delete(sid,cid,qid):
    """
        STABLE - 24/03/2025
        Delete specific quiz.
        DELETE /admin/subjects/:sid/chapters/:cid/quizes

        Expected on success: Specific quiz object removed.
        Additional information: Entry removed from problem table on
        deletion.
    """

    quiz = Quiz.query.filter(Quiz.id == qid).scalar()
    # Validation - Existence
    if quiz is None:
        return jsonify(msg = "No such quiz found!"), 404
    
    try:
        # Cascade deletion deletes entries in problem
        db.session.delete(quiz)
        db.session.commit()

    except Exception as e:
        print(e)
        return jsonify("Quiz deletion failed!"), 400
    
    return jsonify("Quiz deletion success!"), 200