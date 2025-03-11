from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required

admin_response_routes = Blueprint('admin_response_routes', __name__)

# TO DO - Statistics associated with responses

@admin_response_routes.get("/")
@jwt_required()
@admin_required
def admin_view_responses():
    # TO DO - A more powerful way of filtering responses (using input fields in frontend?)
    
    page = request.args.get("page", 1)
    per_page = request.args.get("per_page", 3)
    user_id = request.args.get("user_id", None)
    quiz_id = request.args.get("quiz_id", None)
    question_id = request.args.get("question_id", None)

    try:
        page = int(page)
    except ValueError as e: 
        return jsonify("Bad request! page must be integer"), 400
    
    try:
        per_page = int(per_page)
    except ValueError as e: 
        return jsonify("Bad request! per_page must be integer"), 400
    
    if page <= 0:
        return jsonify("Bad request! page must positive integer"), 400
    
    if per_page <= 0:
        return jsonify("Bad request! per_page must positive integer"), 400
    
    MAX_RESPONSES_PER_PAGE = 5

    r = Response.query
    params = ['user','quiz','question']

    if user_id is not None:
        r = r.filter(Response.user_id == user_id)
        del params[0]

    if quiz_id is not None:
        r = r.filter(Response.quiz_id == quiz_id)
        del params[1]

    if question_id is not None:
        r = r.filter(Response.question_id == question_id)
        del params[2]

    r = r.paginate(page = page, per_page = per_page, max_per_page = MAX_RESPONSES_PER_PAGE)
    return jsonify(payload = [x.serialise(required = params) for x in r]), 200