from flask import Blueprint,jsonify,send_file
from flask_jwt_extended import jwt_required,get_current_user
from api.models import *
from api.blueprints.user import user_required
from api.tasks import triggeredFullReport
import os

# Base URL: /user/summary
user_summary_routes = Blueprint('user_summary_routes', __name__)

@user_summary_routes.get("/")
@jwt_required()
@user_required
def user_get_quiz_summary_csv():
    """
        Endpoint that provides .csv file to be downloaded.
        GET /user/summary/

        Expected on success: On navigation to link, download starts automatically!
    """
    user = get_current_user()
    filename = 'static\\report_{uid}.csv'.format(uid = user.id)

    try:     
        res = send_file(filename, 
            mimetype='text/csv',
            download_name=f'report_{user.name}.csv'
        )
        return res
    
    # Exact exception cannot be provided (WinError?)
    except Exception as e:
        print(e)
        print(e)
        return jsonify(msg = "File does not exist!"),404
    
@user_summary_routes.get("/check")
@jwt_required()
@user_required
def user_check_quiz_summary():
    """
        STABLE - 25/03/2025
        Endpoint that checks for existence of .csv file to be downloaded.
        GET /user/summary/check

        Expected on success: 200 Ok status code with message
    """
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
    """
        STABLE - 25/03/2025
        Endpoint that queues a backend job to generate .csv file
        GET /user/summary/generate

        Expected on success: 200 Ok status code with message. Start of backend job #3
    """
    user = get_current_user()

    base_path = os.getcwd()
    file_path = os.path.join(base_path,"api","static",f"report_{user.id}.csv")
    if os.path.exists(file_path):
        os.remove(file_path)

    triggeredFullReport.delay(user.id)
    return jsonify(msg = "Report generation queued!"),200