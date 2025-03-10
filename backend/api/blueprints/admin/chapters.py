from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required

# Base URL: /admin/subjects/<sid>/chapters
admin_chapter_routes = Blueprint('admin_chapter_routes', __name__)

# TO DO - Remove a chapter?

@admin_chapter_routes.get("/<cid>")
@jwt_required()
@admin_required
def specific_chapter(sid,cid):
    """
        LIVE, STABLE
        See particular chapter information.
        GET /admin/subjects/:sid/chapters/:cid

        Expected on success: Chapter details
        Expected to be handled by frontend:
            404 - Frontend should show not found if chapter not found
    """
    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid).scalar()
    if c:
        return jsonify(payload = c.serialise()), 200
    
    return jsonify(msg = "Subject or chapter not found!"), 404

@admin_chapter_routes.put("/<cid>")
@jwt_required()
@admin_required
def edit_chapter(sid,cid):
    """
        LIVE, STABLE
        Edit particular chapter information.
        PUT /admin/subjects/:sid/chapters/:cid

        Expected on success: Chapter details edited in backend
        Expected to be handled by frontend:
            404 - Frontend should show not found if chapter not found
            400 - Frontend should gracefully handle db errors
    """

    # User input from form
    name = request.form.get("name",None)
    description = request.form.get("description",None)

    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid).scalar()
    if c:
        # Validation for name - Length of name must be > 0
        if name and len(name) > 0:
            c.name = name

        # Validation for description not needed (empty is fine)
        if description:
            c.description = description
        
        # Catch any errors related to database
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify(msg = "Database error encountered!"), 400

        return jsonify(msg = "Chapter edit success!"), 200

    return jsonify(msg = "Subject or chapter not found!"), 404


@admin_chapter_routes.post("/")
@jwt_required()
@admin_required
def add_chapter(sid):
    """
        LIVE, STABLE
        Add a new empty chapter in some subject.
        POST /admin/subjects/:sid/chapters

        Expected on success: Chapter creation in backend
        Expected to be handled by frontend:
            404 - Frontend should show not found if subject not found
            400 - Validation errors
            400 - Database errors
    """
    
    # User input from form
    name = request.form.get("name",None)
    description = request.form.get("description",None)

    # Validation - name should be present
    if name is None:
        return jsonify(msg = "Malformed request! Missing name."), 400
    
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
        return jsonify(msg = "Database error encountered!"), 400
    
    return jsonify(msg = "Chapter creation successful!", payload = c.serialise()), 200
