from functools import wraps
from flask import jsonify,Blueprint
from flask_jwt_extended import get_current_user, jwt_required

user_routes = Blueprint('user_routes', __name__)

def user_required(fun):
    @wraps(fun)
    def inner(*args,**kwargs):
        current_user = get_current_user()
        if current_user.is_admin == 0:
            return fun(*args,**kwargs)
        return jsonify(msg="Not a user!"),400
    return inner


@jwt_required()
@user_required
@user_routes.get("/")
def profile():
    return jsonify(get_current_user().serialise()),200