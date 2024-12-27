from functools import wraps
from flask import jsonify,Blueprint
from flask_jwt_extended import get_current_user

user_routes = Blueprint('user_routes', __name__)

def user_required(fun):
    @wraps(fun)
    def inner(*args,**kwargs):
        current_user = get_current_user()
        if current_user.is_admin == 0:
            return fun(*args,**kwargs)
        return jsonify(msg="Not a user!"),400
    return inner
