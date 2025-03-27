from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required
from sqlalchemy.exc import IntegrityError
from api.blueprints.pagination import pagination_validation
from api import cache

# Base URL : /admin/subjects
admin_subject_routes = Blueprint('admin_subject_routes', __name__)

@admin_subject_routes.get("/")
@jwt_required()
@admin_required
def all_subjects():
    """
        STABLE - 25/03/2025
        See all subjects.
        GET /admin/subjects/

        Expected on success: Paginated, serialised list of filtered subjects
    """
    page = request.args.get("page",1)
    per_page = request.args.get("per_page",5)
    q = request.args.get("q",None)

    MAX_SUBJECTS_PER_PAGE=10
    
    return_val,validation = pagination_validation(page,per_page)
    if validation != 200:
        return validation
    
    page, per_page = return_val

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
@cache.memoize(10)
def specific_subject(id):
    """
        STABLE - 25/03/2025
        See specific subject.
        GET /admin/subjects/:id

        Expected on success: Payload is serailised subject with chapter (required)
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

        Expected on success: Edit details of subject object in db.
    """

    name = request.form.get("name", None)
    description = request.form.get("description", None)

    # Valdiation - existence
    s = Subject.query.filter(Subject.id == id).scalar()
    if s:
        cache.delete_memoize(specific_subject,id)
        # Validation - Name should be non empty
        try:
            if name and len(name) > 0:
                s.name = name
            
            # Validation - Description
            if description is not None:
                s.description = description
            
            db.session.commit()

        except IntegrityError as e:
            return jsonify(msg="Subject with that name already exists!"),400

        return jsonify(msg="Edit subject success"),200
    
    return jsonify(msg="No such subject found!"),400

@admin_subject_routes.post("/")
@jwt_required()
@admin_required
def add_subject():
    """
        STABLE - 25/03/2025
        Add new subject.
        POST /admin/subjects

        Expected on success: Creation of new subject object in db
    """
    name = request.form.get("name",None)
    description = request.form.get("description",None)
    
    # Validation : name is non empty
    if name is None or len(name) == 0:
        return jsonify(msg="Malformed request: Check if all fields included"),400
    
    s = Subject(name = name, description = description)
    try:
        db.session.add(s)
        db.session.commit()
        return jsonify(msg="Subject creation successful",payload=s.serialise()),200
    
    except IntegrityError as e:
        return jsonify(msg="Subject already exists!"),400
    
@admin_subject_routes.delete("/<sid>")
@jwt_required()
@admin_required
def admin_delete_subject(sid):
    """
        STABLE - 25/03/2025
        Add new subject.
        DELETE /admin/subjects/:sid

        Expected on success: Deletion of specific subject object from db.
        Additional information: Deletion of subject deletes all chapters underneath
        it along with all the quizes, questions underneath each chapter, all responses
        for any quiz-question, any score objects, all enrollments to subject, and all 
        requested entries.
    """

    subject = Subject.query.filter(Subject.id == sid).scalar()
    # Validation - existence
    if subject is None:
        return jsonify(msg= "No such subject found!"),404
    
    try: 
        # Cascade handles all the required logic!
        db.session.delete(subject)
        db.session.commit()
    
    except Exception as e:
        print(e)
        return jsonify(msg = "subject deletion failed!"),400
    
    return jsonify(msg="subject deletion success!"),200