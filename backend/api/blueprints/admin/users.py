# STABLE - 25/03/2025

from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required
from api.blueprints.pagination import pagination_validation
from api import cache

# Base URL: /admin/users
admin_user_routes = Blueprint('admin_user_routes', __name__)

@admin_user_routes.get("/")
@jwt_required()
@admin_required
def all_users():
    """
        STABLE - 25/03/2025
        See all users.
        GET /admin/users/

        Expected on success: Serialised, paginated list of filtered users
    """

    page = request.args.get("page", 1)
    per_page = request.args.get("per_page", 5)
    q = request.args.get("q", None)

    return_val,validation = pagination_validation(page,per_page)
    if validation != 200:
        return validation
    
    page, per_page = return_val

    # Arbitrary constant on max allowed amount of users
    # If per_page >= MAX_USERS_PER_PAGE then a page contains MAX_USERS_PER_PAGE items only
    MAX_USERS_PER_PAGE = 10

    # Searching for all users
    if q:
        query = User.query.filter(
                User.is_admin == 0, 
                User.name.ilike(f"%{q}%")
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
@cache.memoize(10)
def specific_users(id):
    """
        STABLE - 25/03/2025
        See specific user.
        GET /admin/users/:id

        Expected on success: Serialised user details with subjects (non-paginated!)
    """

    # Admin user cannot be seen
    u = User.query.filter(User.id == id, User.is_admin == 0).scalar()
    if u:
        return jsonify(payload=u.serialise(required=['subjects']))
    return jsonify(msg="No such user found!"),404
