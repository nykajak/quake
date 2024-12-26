from api import app,db,bcrypt
from api.models import *
from flask import request, jsonify
from flask_jwt_extended import create_access_token,jwt_required,set_access_cookies,unset_jwt_cookies
from sqlalchemy.exc import IntegrityError

@app.get("/")
def home():
    return jsonify(msg="Hello world!")

@app.get("/all")
@jwt_required()
def all():
    l = User.query.filter()
    res = []
    for x in l:
        res.append(
            {
                "name" : x.name,
            }
        )
    return jsonify(payload = res)

from api.blueprints.anon.anon_routes import anon_routes
app.register_blueprint(anon_routes)