from functools import wraps
from flask import jsonify,Blueprint
from flask_jwt_extended import get_current_user

admin_routes = Blueprint('admin_routes', __name__)

def admin_required(fun):
    @wraps(fun)
    def inner(*args,**kwargs):
        current_user = get_current_user()
        if current_user.is_admin == 1:
            return fun(*args,**kwargs)
        return jsonify(msg="Not an Admin!"),400
    return inner

from api.blueprints.admin.users import user_routes
from api.blueprints.admin.subjects import subject_routes

admin_routes.register_blueprint(user_routes,url_prefix = "/users")
admin_routes.register_blueprint(subject_routes,url_prefix = "/subjects")