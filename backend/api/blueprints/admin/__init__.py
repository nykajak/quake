from functools import wraps
from api.models import *
from flask import jsonify,Blueprint
from flask_jwt_extended import get_current_user

# All admin endpoints start with /admin
admin_routes = Blueprint('admin_routes', __name__, url_prefix="/admin")

# Decorator to ensure that endpoint accessed by admin user only
def admin_required(fun):
    @wraps(fun)
    def inner(*args,**kwargs):
        current_user = get_current_user()
        if current_user.is_admin == 1:
            return fun(*args,**kwargs)
        return jsonify(msg="Not an Admin!"),400
    return inner

# Importing required functionality related to admin responsibilites
from api.blueprints.admin.users import admin_user_routes
from api.blueprints.admin.subjects import admin_subject_routes
from api.blueprints.admin.chapters import admin_chapter_routes
from api.blueprints.admin.questions import admin_question_routes
from api.blueprints.admin.quizes import admin_quiz_routes
from api.blueprints.admin.enrolled import admin_enrolled_routes
from api.blueprints.admin.responses import admin_response_routes
from api.blueprints.admin.scores import admin_score_routes

# User related endpoints: /admin/users
admin_routes.register_blueprint(admin_user_routes, url_prefix="/users")

# Subject related endpoints: /admin/subjects
admin_routes.register_blueprint(admin_subject_routes, url_prefix="/subjects")

# Response related endpoints: /admin/responses
admin_routes.register_blueprint(admin_response_routes, url_prefix="/responses")

# Enrollment related endpoints: /admin/enrolled
admin_routes.register_blueprint(admin_enrolled_routes,url_prefix = "/enrolled")

# Chapter related endpoints: /admin/subjects/<sid>/chapters
admin_subject_routes.register_blueprint(admin_chapter_routes,url_prefix = "/<sid>/chapters")

# Question related endpoints: /admin/subjects/<sid>/chapters/<cid>/questions
admin_chapter_routes.register_blueprint(admin_question_routes,url_prefix = "/<cid>/questions")

# Quiz related endpoints: /admin/subjects/<sid>/chapters/<cid>/quizes
admin_chapter_routes.register_blueprint(admin_quiz_routes,url_prefix = "/<cid>/quizes")

# Score related endpoints: /admin/scores
admin_routes.register_blueprint(admin_score_routes, url_prefix="/scores")