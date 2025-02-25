from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required

admin_chapter_routes = Blueprint('admin_chapter_routes', __name__)

@admin_chapter_routes.get("/<cid>")
@jwt_required()
@admin_required
def specific_chapter(sid,cid):
    """
        LIVE
        See particular chapter information.
        GET /admin/subjects/:sid/chapters/:cid

        Expected on success: Chapter details
    """
    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid).scalar()
    if c:
        return jsonify(payload = c.serialise())
    
    return jsonify(msg="Subject or chapter not found!"),400

@admin_chapter_routes.put("/<cid>")
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


@admin_chapter_routes.post("/")
@jwt_required()
@admin_required
def add_chapter(sid):
    """
        Add chapter.
        POST /admin/subjects/:sid/chapters

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
