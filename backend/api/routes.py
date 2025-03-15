from api import app,db,bcrypt,jwt
from api.models import *
from flask import request, jsonify
from flask_jwt_extended import jwt_required,current_user,get_jwt,create_access_token,get_jwt_identity,set_access_cookies
from sqlalchemy.exc import IntegrityError
from datetime import datetime,timedelta

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter(User.name == identity).scalar()

@app.errorhandler(404)
def page_not_found(e):
    resp = jsonify(msg="Page not found!")
    return resp,404

# Optionally add error handler for 401 - unauthorised errors

@app.after_request
def refresh_tokens(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now()

        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response

    except (RuntimeError, KeyError):
        return response

@app.get("/")
@jwt_required(optional=True)
def home():
    """
        LIVE
        Check to see current role and permissions of logged in user.
        GET /

        Expected on success: Response with suitable msg and role attributes.
    """
    if current_user:
        role = "user" if current_user.is_admin == 0 else "admin"
        return jsonify(msg = f"Hello {current_user.name}!", role = role)
    
    return jsonify(msg = "Hello anonymous person!", role = "anon")

from api.blueprints.anon import anon_routes
from api.blueprints.admin import admin_routes
from api.blueprints.user import user_routes

app.register_blueprint(anon_routes)
app.register_blueprint(admin_routes, url_prefix = "/admin")
app.register_blueprint(user_routes, url_prefix = "/user")