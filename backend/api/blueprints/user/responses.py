from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required,get_current_user
from api.models import *
from api.blueprints.user import user_required

user_response_routes = Blueprint('user_response_routes', __name__)

# Note: Remove redundant file?