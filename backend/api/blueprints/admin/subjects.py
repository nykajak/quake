# Stable API

from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required
from sqlalchemy.exc import IntegrityError

admin_subject_routes = Blueprint('admin_subject_routes', __name__)

# TO DO - Subject deletion?

@admin_subject_routes.get("/")
@jwt_required()
@admin_required
def all_subjects():
    """
        DONE
        See all subjects.
        GET /admin/subjects/

        Query string args: page, per_page and q (for pagination and filtering)

        Expected on success: List of all subjects according to query.
    """
    page = request.args.get("page",1)
    per_page = request.args.get("per_page",5)
    q = request.args.get("q",None)

    MAX_SUBJECTS_PER_PAGE=10
    
    # Validation
    try:
        page = int(page)
    except ValueError as e:
        return jsonify(msg = "Bad request! page should be integer")

    try:
        per_page = int(per_page)
    except ValueError as e:
        return jsonify(msg = "Bad request! per_page should be integer")
    
    if page <= 0:
        return jsonify(msg = "Bad request! page should be positive integer")

    # Database query
    if not q:
        query = Subject.query.filter().paginate(page=page,per_page=per_page,max_per_page=MAX_SUBJECTS_PER_PAGE)
    else:
        query = Subject.query.filter(Subject.name.startswith(q)).paginate(page=page,per_page=per_page,max_per_page=MAX_SUBJECTS_PER_PAGE)
    
    res = [s.serialise() for s in query]
    return jsonify(payload=res,pages=query.pages)

@admin_subject_routes.get("/<id>")
@jwt_required()
@admin_required
def specific_subject(id):
    """
        DONE
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
        DONE
        Edit subject.
        POST /admin/subjects

        Request body: name,description

        Expected on success: Modification of existing subject.
    """

    name = request.form.get("name", None)
    description = request.form.get("description", None)

    s = Subject.query.filter(Subject.id == id).scalar()
    if s:
        try:
            if name and len(name) > 0:
                s.name = name
            
            if description:
                s.description = description
            
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
        DONE
        Add new subject.
        POST /admin/subjects

        Request body: name,description

        Expected on success: Creation of new Subject in db
    """
    name = request.form.get("name",None)
    description = request.form.get("description",None)
    

    if name is None or len(name) == 0:
        return jsonify(msg="Malformed request: Check if all fields included"),400
    
    
    s = Subject(name = name, description = description)
    try:
        db.session.add(s)
        db.session.commit()
        return jsonify(msg="Subject creation successful",payload=s.serialise()),200
    
    except IntegrityError as e:
        return jsonify(msg="Subject already exists!"),400