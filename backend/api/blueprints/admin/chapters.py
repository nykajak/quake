# STABLE - 24/03/2025

from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api import cache
from api.models import *
from api.blueprints.admin import admin_required

# Base URL: /admin/subjects/<sid>/chapters
admin_chapter_routes = Blueprint('admin_chapter_routes', __name__)

@admin_chapter_routes.get("/<cid>")
@jwt_required()
@admin_required
@cache.memoize(10)
def admin_view_specific_chapter(sid,cid):
    """
        STABLE - 24/03/2025
        See particular chapter information.
        GET /admin/subjects/:sid/chapters/:cid

        Expected on success: Return specific chapter in serialised form as payload.
    """
    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid).scalar()
    if c:
        return jsonify(payload = c.serialise()), 200
    
    return jsonify(msg = "Subject or chapter not found!"), 404

@admin_chapter_routes.put("/<cid>")
@jwt_required()
@admin_required
def admin_edit_chapter(sid,cid):
    """
        STABLE - 24/03/2025
        Edit particular chapter information.
        PUT /admin/subjects/:sid/chapters/:cid

        Expected on success: Chapter details edited
        Additional information: If name does not pass validation check then no 
        edit happens for that attribute alone!
    """

    # User input from form
    name = request.form.get("name",None)
    description = request.form.get("description",None)

    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid).scalar()
    if c:
        cache.delete_memoized(admin_view_specific_chapter,sid,cid)

        # Validation for name - Length of name must be > 0
        if name is not None and len(name) > 0:
            c.name = name

        # Validation for description not needed (empty is fine)
        if description is not None:
            c.description = description
        
        # Catch any errors related to database
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify(msg = "Database error encountered!"), 500

        return jsonify(msg = "Chapter edit success!"), 200

    return jsonify(msg = "Chapter not found!"), 404


@admin_chapter_routes.post("/")
@jwt_required()
@admin_required
def admin_add_chapter(sid):
    """
        STABLE - 24/03/2025
        Add a new empty chapter in some subject.
        POST /admin/subjects/:sid/chapters

        Expected on success: Chapter creation in backend and serialised chapter 
        returned as payload.
    """
    
    # User input from form
    name = request.form.get("name",None)
    description = request.form.get("description",None)

    # Validation - name should be present
    if name is None or len(name) == 0:
        return jsonify(msg = "Malformed request! Missing name."), 400
    
    # Validation - description should be present
    if description is None:
        return jsonify(msg = "Malformed request! Missing description."), 400
    
    # Validation - subject found?
    s = Subject.query.filter(Subject.id == sid).scalar()
    if s is None:
        return jsonify(msg = "Subject not found!"), 404
    
    c = Chapter(name = name, description = description, subject_id = sid)
    db.session.add(c)

    # Catch any errors related to database
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify(msg = "Database error encountered!"), 500
    
    return jsonify(msg = "Chapter creation successful!", payload = c.serialise()), 200

@admin_chapter_routes.delete("/<cid>")
@jwt_required()
@admin_required
def admin_delete_chapter(sid,cid):
    """
        STABLE - 24/03/2025
        Delete a specific chapter.
        DELETE /admin/subjects/:sid/chapters/:cid

        Expected on success: Chapter deletion in backend.
        Additional information: When chapter is deleted, all quizes and
        questions under it are also deleted. This triggers deletion of
        all responses associated with quizes/questions, scores associated
        with quizes belonging to given chapter.
    """

    # Validation: Check for existence of chapter
    chapter = Chapter.query.filter(Chapter.id == cid).scalar()
    if chapter is None:
        return jsonify(msg= "No such chapter found!"),404
    
    try:
        # Delete cascade defined in models. Nothing to handle here! 
        db.session.delete(chapter)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify(msg = "Chapter deletion failed!"),400
    
    return jsonify(msg="Chapter deletion success!"),200
