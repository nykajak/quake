from functools import wraps
from flask import jsonify,Blueprint
from flask_jwt_extended import get_current_user

admin_routes = Blueprint('admin_routes', __name__, url_prefix="/admin")

def admin_required(fun):
    @wraps(fun)
    def inner(*args,**kwargs):
        current_user = get_current_user()
        if current_user.is_admin == 1:
            return fun(*args,**kwargs)
        return jsonify(msg="Not an Admin!"),400
    return inner

from api.blueprints.admin.users import admin_user_routes
from api.blueprints.admin.subjects import admin_subject_routes

admin_routes.register_blueprint(admin_user_routes)
admin_routes.register_blueprint(admin_subject_routes)