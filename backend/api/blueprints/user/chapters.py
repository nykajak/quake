from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required,get_current_user
from api.models import *
from api.blueprints.user import user_required
from datetime import datetime
from api.blueprints.pagination import pagination_validation

user_chapter_routes = Blueprint('user_chapter_routes', __name__)

@user_chapter_routes.get("/<cid>")
@jwt_required()
@user_required
def user_specific_chapter(sid,cid):

    filter_ = request.args.get("filter", "pending")
    page = request.args.get("page", 1)
    per_page = request.args.get("per_page", 3)

    return_val,validation = pagination_validation(page,per_page)
    if validation != 200:
        return validation
    
    page, per_page = return_val

    MAX_QUIZES_PER_PAGE = 10

    u = get_current_user()
    c = Chapter.query.filter(Chapter.id == cid, Chapter.subject_id == sid).scalar()

    if c is None:
        return jsonify(msg = "Chapter not found!"), 400
    
    if c.subject not in u.subjects:
        return jsonify(msg = "User not registered for subject!"),400

    if filter_ not in ('pending','past'):
        return jsonify(msg = "Bad request, filter does not exist"), 400
    
    if filter_ == 'pending':
        query = c.quizes.filter(Quiz.dated > datetime.now()).paginate(page=page,per_page=per_page,max_per_page=MAX_QUIZES_PER_PAGE)
        quizes = [x.serialise() for x in query]
    else:
        query = c.quizes.filter(Quiz.dated < datetime.now()).paginate(page=page,per_page=per_page,max_per_page=MAX_QUIZES_PER_PAGE)
        quizes = [x.serialise() for x in query]
        
    return jsonify(payload=c.serialise(),quizes = quizes, pages = query.pages),200