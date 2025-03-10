from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError

# Base URL: /admin/enrolled
admin_enrolled_routes = Blueprint('admin_enrolled_routes', __name__)

@admin_enrolled_routes.get("/requests")
@jwt_required()
@admin_required
def see_requests():
    """
        LIVE, STABLE
        See all pending requests for enrollment.
        GET /admin/enrolled/requests

        Expected on success: Payload containing all requests
        Expected to be handled by frontend:
            200 - Empty payload, frontend should render some message
    """
    
    # TO DO - Pagination of results

    # Note: Order of objects in query important as referenced in payload
    query = db.session.query(Requested, User, Subject).join(User,  Requested.user_id == User.id).join(Subject,  Requested.subject_id == Subject.id)
    payload = [
        {
            "user": x[1].serialise(),
            "subject": x[2].serialise()
        } for x in query
    ]

    return jsonify(payload = payload), 200

@admin_enrolled_routes.get("/subjects/<sid>")
@jwt_required()
@admin_required
def see_enrolled(sid):
    """
        LIVE
        See all students enrolled for subject.
        POST /admin/enrolled/subjects/:sid

        Expected on success: Paginated list of users enrolled for subject
        Expected to be handled by frontend:
            200 - Empty payload, frontend should render some message
    """
    page = request.args.get("page", 1)
    per_page = request.args.get("per_page", 5)

    try:
        page = int(page)
        per_page = int(per_page)

        if page <= 0:
            return jsonify(msg="Bad request: page has to be postiive integer!"), 400

        if per_page <= 0:
            return jsonify(msg="Bad request: per_page has to be postiive integer!"), 400

    except ValueError as e:
        return jsonify(msg="Bad request: page and per_page have to be integers!"), 400
    
    s = Subject.query.filter(Subject.id == sid).scalar()
    if s:
        MAX_USERS_PER_PAGE = 10
        query = s.users.paginate(page = page, per_page = per_page, max_per_page = MAX_USERS_PER_PAGE)
        users = [x.serialise() for x in query]
        return jsonify(payload = {"users":users}, pages = query.pages), 200
    
    return jsonify(msg = "No such subject found!"), 400


@admin_enrolled_routes.post("users/<uid>/subjects/<sid>")
@jwt_required()
@admin_required
def add_user_to_subject(uid,sid):
    """
        LIVE, STABLE
        Enroll user in subject.
        POST /admin/enrolled/users/:id/subjects/:sid

        Expected on success: User gains access to subject
        Expected to be handled by frontend:
            404 - No such user/subject
            400 - No such request
            400 - Database error
            200 - Already enrolled!
    """

    r = Requested.query.filter(Requested.user_id == uid, Requested.subject_id == sid).scalar()
    if r:
        db.session.delete(r)
        db.session.commit()
    
    else:
        return jsonify(msg = "Cannot enroll user in absence of request!"), 400

    # Cannot enroll admin user
    u = User.query.filter(User.id == uid, User.is_admin == 0).scalar()
    s = Subject.query.filter(Subject.id == sid).scalar()
    
    if u and s:
        try:
            u.subjects.append(s)
            db.session.commit()
            return jsonify(msg = "Added subject!"), 200
        
        except IntegrityError as e:
            return jsonify(msg = "Already enrolled!"), 200
        
        except Exception as e:
            print(e)
            return jsonify(msg = "Database error!"), 400
        
    return jsonify(msg="No such user or subject found!"), 404

@admin_enrolled_routes.delete("/users/<uid>/subjects/<sid>")
@jwt_required()
@admin_required
def remove_user_from_subject(uid,sid):
    """
        LIVE, STABLE
        Un-enroll user in subject.
        DELETE /admin/enrolled/users/:id/subjects/:sid

        Expected on success: User loses access to subject
        Expected to be handled by frontend:
            404 - No such user/subject
            200 - User already not enrolled
            400 - Database error
    """

    r = Requested.query.filter(Requested.user_id == uid, Requested.subject_id == sid).scalar()
    if r:
        db.session.delete(r)
        db.session.commit()
    
    # Admin user can't be enrolled!
    u = User.query.filter(User.id == uid, User.is_admin == 0).scalar()
    s = Subject.query.filter(Subject.id == sid).scalar()

    if u and s:
        try:
            u.subjects.remove(s)
            db.session.commit()
            return jsonify(msg = "Subject removed from user enrollment!"), 200

        except StaleDataError as e:
            return jsonify(msg = "User is not enrolled!"), 200
        
        except Exception as e:
            print(e)
            return jsonify(msg = "Database error!"), 400
        
    return jsonify(msg = "No such user or subject found!"), 400

