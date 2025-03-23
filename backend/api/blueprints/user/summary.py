from flask import Blueprint,jsonify,send_file
from flask_jwt_extended import jwt_required,get_current_user
from api.models import *
from api.blueprints.user import user_required
from api.tasks import export_csv
import os

user_summary_routes = Blueprint('user_summary_routes', __name__)

@user_summary_routes.get("/")
@jwt_required()
@user_required
def user_get_quiz_summary_csv():
    user = get_current_user()
    filename = 'static\\report_{uid}.csv'.format(uid = user.id)

    try:     
        res = send_file(filename, 
            mimetype='text/csv',
            download_name=f'report_{user.name}.csv'
        )
        return res
    except Exception as e:
        print(e)
        return jsonify(msg = "File does not exist!"),404
    
@user_summary_routes.get("/check")
@jwt_required()
@user_required
def user_check_quiz_summary():
    user = get_current_user()
    
    base_path = os.getcwd()
    file_path = os.path.join(base_path,"api","static",f"report_{user.id}.csv")
    if os.path.exists(file_path):
        return jsonify(msg = "File generation complete!"),200
    
    return jsonify(msg = "File does not exist"),404

@user_summary_routes.get("/generate")
@jwt_required()
@user_required
def user_generate_quiz_summary():
    user = get_current_user()

    base_path = os.getcwd()
    file_path = os.path.join(base_path,"api","static",f"report_{user.id}.csv")
    if os.path.exists(file_path):
        os.remove(file_path)

    export_csv.delay(user.id)
    return jsonify(msg = "Report generation queued!"),200