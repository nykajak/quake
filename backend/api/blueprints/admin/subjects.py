from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required
from sqlalchemy.exc import IntegrityError

subject_routes = Blueprint('subject_routes', __name__)

@subject_routes.get("/")
@jwt_required()
@admin_required
def all_subjects():
    page = int(request.args.get("page",1))
    per_page = int(request.args.get("per_page",5))

    query = Subject.query.filter().paginate(page=page,per_page=per_page,max_per_page=10)
    res = [s.serialise() for s in query]
    
    return jsonify(payload=res)

@subject_routes.get("/<id>")
@jwt_required()
@admin_required
def specific_subjects(id):
    s = Subject.query.filter(Subject.id == id).scalar()
    if s:
        return jsonify(payload=s.serialise())
    
    return jsonify(msg="No such subject found!"),400

@subject_routes.post("/")
@jwt_required()
@admin_required
def add_subject():
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
    
@subject_routes.get("/<id>/chapters")
@jwt_required()
@admin_required
def all_chapters(id):
    s = Subject.query.filter(Subject.id == id).scalar()
    if s:
        return jsonify(payload = s.serialise(required=("chapters")))
    
    return jsonify(msg="Subject not found!"),400

@subject_routes.get("/<sid>/chapters/<cid>")
@jwt_required()
@admin_required
def specific_chapter(sid,cid):
    s = Subject.query.filter(Subject.id == sid).scalar()
    c = Chapter.query.filter(Chapter.id == cid).scalar()
    if s and c:
        if c in s.chapters:
            return jsonify(payload = c.serialise())
    
    return jsonify(msg="Subject or chapter not found!"),400

@subject_routes.post("/<sid>/chapters")
@jwt_required()
@admin_required
def add_chapter(sid):
    s = Subject.query.filter(Subject.id == sid).scalar()
    if s is None:
        return jsonify(msg="Subject not found!"),400
    
    name = request.form.get("name",None)
    description = request.form.get("description",None)

    if name is None:
        return jsonify(msg="Malformed request!"),400
    
    c = Chapter(name = name, description = description, subject_id = sid)
    db.session.add(c)
    db.session.commit()
    
    return jsonify(msg="Chapter created!"),200

@subject_routes.get("/<sid>/chapters/<cid>/quizes")
@jwt_required()
@admin_required
def all_quizes(sid,cid):
    s = Subject.query.filter(Subject.id == sid).scalar()
    c = Chapter.query.filter(Chapter.id == cid).scalar()
    if s and c:
        if c in s.chapters:
            return jsonify(payload = c.serialise(required=("quizes")))
    
    return jsonify(msg="Subject or chapter not found!"),400

@subject_routes.post("/<sid>/chapters/<cid>/quizes")
@jwt_required()
@admin_required
def add_quiz(sid,cid):
    s = Subject.query.filter(Subject.id == sid).scalar()
    c = Chapter.query.filter(Chapter.id == cid).scalar()
    if s and c:
        dated = request.form.get("dated",None)
        duration = request.form.get("duration",None)
        description = request.form.get("description",None)

        if dated is None or duration is None:
            return jsonify(msg="Malformed request!"),400    

        q = Quiz(chapter_id = cid, dated = dated, duration = duration, description = description)
        return jsonify(msg="Quiz added!"),200
    
    return jsonify(msg="Subject or chapter not found!"),400

@subject_routes.get("/<sid>/chapters/<cid>/quizes/<qid>")
@jwt_required()
@admin_required
def specific_quiz(sid,cid,qid):
    s = Subject.query.filter(Subject.id == sid).scalar()
    c = Chapter.query.filter(Chapter.id == cid).scalar()
    q = Quiz.query.filter(Quiz.id == qid).scalar()

    if s and c:
        if c in s.chapters and q in c.quizes:
            return jsonify(payload = q.serialise())
    
    return jsonify(msg="Subject, chapter or quiz not found!"),400