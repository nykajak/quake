from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required
from api.models import *
from api.blueprints.admin import admin_required
from api.blueprints.pagination import pagination_validation

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

    return_val,validation = pagination_validation(page,per_page)
    if validation != 200:
        return validation
    
    page, per_page = return_val
    
    MAX_RESPONSES_PER_PAGE = 5

    r = Response.query
    params = set(['user','quiz','question'])

    if user_id is not None:
        r = r.filter(Response.user_id == user_id)
        params.remove('user')

    if quiz_id is not None:
        r = r.filter(Response.quiz_id == quiz_id)
        params.remove('quiz')

    if question_id is not None:
        r = r.filter(Response.question_id == question_id)
        params.remove('question')

    r = r.paginate(page = page, per_page = per_page, max_per_page = MAX_RESPONSES_PER_PAGE)
    return jsonify(payload = [x.serialise(required = params) for x in r], pages = r.pages), 200