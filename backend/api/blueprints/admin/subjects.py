from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required
from sqlalchemy.exc import IntegrityError

from datetime import datetime, timedelta

admin_subject_routes = Blueprint('admin_subject_routes', __name__)
# Split up file into smaller files - subject, chapter, quiz, question etc
# Error handling and graceful fail states
# Documentation

@admin_subject_routes.get("/")
@jwt_required()
@admin_required
def all_subjects():
    """
        LIVE
        See all subjects.
        GET /admin/subjects/

        Query string args: page, per_page and q (for pagination and filtering)

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
        GET /admin/subjects/:id

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
    """
        Edit subject.
        POST /admin/subjects

        Request body: name,description,credits

        Expected on success: Modification of existing subject.
    """

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
                    if credits > 0:
                        s.credits = credits

                    else:
                        return jsonify(msg="Malformed request: Credits field should be greater than 0"),400

                except ValueError as e:
                    return jsonify(msg="Malformed request: Credits field should be integer"),400
            
            db.session.commit()

        except Exception as e:
            return jsonify(msg="Subject with that name already exists!"),400

        return jsonify(msg="Edit subject success"),200
    
    return jsonify(msg="No such subject found!"),400

@admin_subject_routes.post("/")
@jwt_required()
@admin_required
def add_subject():
    """
        Add new subject.
        POST /admin/subjects

        Request body: name,description,credits

        Expected on success: Creation of new Subject in db
    """
    name = request.form.get("name",None)
    description = request.form.get("description",None)
    
    credits = request.form.get("credits",0)
    try:
        credits = int(credits)
    except:
        return jsonify(msg="Malformed request: Credits field should be integer"),400

    if name is None or len(name) == 0:
        return jsonify(msg="Malformed request: Check if all fields included"),400
    
    if credits <= 0:
        return jsonify(msg="Malformed request: Credits field should be greater than 0"),400
    
    s = Subject(name = name, credits = credits, description = description)
    try:
        db.session.add(s)
        db.session.commit()
        return jsonify(msg="Subject creation successful",payload=s.serialise()),200
    
    except IntegrityError as e:
        return jsonify(msg="Subject already exists!"),400
    
@admin_subject_routes.get("/<sid>/enrolled")
@jwt_required()
@admin_required
def see_enrolled(sid):
    """
        LIVE
        See all students enrolled for subject.
        POST /admin/subjects/:sid/enrolled

        Expected on success: List of users enrolled for subject
    """
    s = Subject.query.filter(Subject.id == sid).scalar()
    if s:
        return jsonify(payload=s.serialise(required=['users']))
    
    return jsonify(msg="No such subject found!"),400