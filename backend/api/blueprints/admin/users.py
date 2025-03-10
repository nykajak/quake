from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required

admin_user_routes = Blueprint('admin_user_routes', __name__)

# Error handling and graceful fail states

@admin_user_routes.get("/")
@jwt_required()
@admin_required
def all_users():
    """
        LIVE
        See all users.
        GET /admin/users/

        Query string args: page, per_page and q (for filtering)

        Expected on success: List of all users according to query.
        Expected to be handled by frontend:
            Error code 400 - Bad request
            Error code 404 - If page that does not exist is queried
            Empty list as payload
    """

    page = request.args.get("page", 1)
    per_page = request.args.get("per_page", 5)
    q = request.args.get("q", None)

    # Validation - Check if page and per_page are integers
    try:
        page = int(page)

    except ValueError as e:
        return jsonify(msg = "Bad request - page should be a postive integer"), 400

    try:
        per_page = int(per_page)

    except ValueError as e:
        return jsonify(msg = "Bad request - per_page should be a postive integer"), 400
    
    # Validation - Check if page and per_page are non-zero and positive integers
    if page <= 0:
        return jsonify(msg = "Bad request - page should be a postive integer"), 400

    if per_page <= 0:
        return jsonify(msg = "Bad request - per_page should be a postive integer"), 400

    # Arbitrary constant on max allowed amount of users
    # If per_page >= MAX_USERS_PER_PAGE then a page contains MAX_USERS_PER_PAGE items only
    MAX_USERS_PER_PAGE = 10

    # Searching for all users

    if q:
        query = User.query.filter(
                User.is_admin == 0, 
                User.name.startswith(q)
            ).paginate(
                page = page,
                per_page = per_page,
                max_per_page = MAX_USERS_PER_PAGE
        )
    else:
        query = User.query.filter(
                User.is_admin == 0
            ).paginate(
                page = page,
                per_page = per_page,
                max_per_page = MAX_USERS_PER_PAGE
        )
    
    # Returned payload may be empty list - Should be handled in frontend
    res = [u.serialise() for u in query]
    return jsonify(payload=res,pages=query.pages), 200

@admin_user_routes.get("/<id>")
@jwt_required()
@admin_required
def specific_users(id):
    """
        LIVE
        See specific user.
        GET /admin/users/:id

        Expected on success: Specific user details with subject information
        Expected to be handled by frontend:
            Error code 404 - If no such user exists
            Empty list of subjects returned
    """

    # Admin user cannot be seen
    u = User.query.filter(User.id == id, User.is_admin == 0).scalar()
    if u:
        return jsonify(payload=u.serialise(required=['subjects']))
    return jsonify(msg="No such user found!"),404



@admin_user_routes.get("/<id>/scores")
@jwt_required()
@admin_required
def specific_users_scores(id):
    """
        Retreive user scores.
        GET /admin/users/:id/scores

        Expected on success: Summary of user scores
    """
    
    # TO DO - Add functionality for getting summary of user scores!
    u = User.query.filter(User.id == id).scalar()
    if u:
        return jsonify(payload=u.serialise(required = ("scores")))
    return jsonify(msg="No such user found!"),400



@admin_user_routes.get("/<id>/responses")
@jwt_required()
@admin_required
def specific_users_responses(id):
    """
        Retreive user responses.
        GET /admin/users/:id/responses

        Expected on success: User details and list of user responses
    """
    
    # TO DO - Implement pagination in user responses!    
    u = User.query.filter(User.id == id).scalar()
    if u:
        return jsonify(payload=u.serialise(required = ("responses")))
    return jsonify(msg="No such user found!"),400