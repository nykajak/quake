from functools import wraps
from flask import jsonify, Blueprint
from flask_jwt_extended import get_current_user, jwt_required
from api.models import *

# All admin endpoints start with /user
user_routes = Blueprint('user_routes', __name__)

# Wrapper to make sure sender is a user
def user_required(fun):
    @wraps(fun)
    def inner(*args,**kwargs):
        current_user = get_current_user()
        if current_user.is_admin == 0:
            return fun(*args,**kwargs)
        return jsonify(msg="Not a user!"),400
    return inner

@user_routes.get("/")
@jwt_required()
@user_required
def profile():
    """
        STABLE - 25/03/2025
        Returns currently logged in user details
        GET /user/

        Expected on success: Serialised details of current user
    """
    u = get_current_user()
    return jsonify(payload=u.serialise()),200

# Importing required functionality related to user responsibilites
from api.blueprints.user.subjects import user_subject_routes
from api.blueprints.user.enrolled import user_enrolled_routes
from api.blueprints.user.chapters import user_chapter_routes
from api.blueprints.user.quizes import user_quiz_routes
from api.blueprints.user.questions import user_question_routes
from api.blueprints.user.responses import user_response_routes
from api.blueprints.user.summary import user_summary_routes

# Subject related endpoints: /user/subjects
user_routes.register_blueprint(user_subject_routes, url_prefix = '/subjects')

# Enrollment related endpoints: /user/enrolled
user_routes.register_blueprint(user_enrolled_routes, url_prefix = '/enrolled')

# Response related endpoints: /user/responses
user_routes.register_blueprint(user_response_routes, url_prefix = '/responses')

# Summary related endpoints: /user/summary
user_routes.register_blueprint(user_summary_routes, url_prefix = '/summary')

# Chapter related endpoints: /user/subjects/:sid/chapters
user_subject_routes.register_blueprint(user_chapter_routes, url_prefix = '/<sid>/chapters')

# Chapter related endpoints: /user/subjects/:sid/chapters/:cid/quizes
user_chapter_routes.register_blueprint(user_quiz_routes, url_prefix = '/<cid>/quizes')

# Question related endpoints: /user/subjects/:sid/chapters/:cid/quizes/:qid/questions
user_quiz_routes.register_blueprint(user_question_routes, url_prefix = '/<quiz_id>/questions')