from api import app,db,bcrypt
from flask import Blueprint,request,jsonify
from flask_jwt_extended import create_access_token,set_access_cookies,unset_jwt_cookies
from sqlalchemy.exc import IntegrityError
from api.models import *

anon_routes = Blueprint('anon_routes', __name__)

@anon_routes.post("/login")
def login():
    username = request.form.get("username",None)
    password = request.form.get("password",None)

    if not username or not password:
        return jsonify(msg="Malformed request: Check if both username and passowrd included"),401
    
    res = User.query.filter(User.name == username).scalar()
    flag = True if res and res.is_admin == 1 else 0

    if res:
        res = bcrypt.check_password_hash(res.password,password)

    if res:
        if flag:    
            response = jsonify(msg="Authentication success",payload='admin')
        else:
            response = jsonify(msg="Authentication success",payload='user')
            
        access_token = create_access_token(identity=username)
        set_access_cookies(response,access_token)
        return response,200

    return jsonify(msg="Authentication failed!"),401

@anon_routes.post("/logout")
def logout():
    response = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(response)
    return response,200

@anon_routes.post("/register")
def register():
    username = request.form.get("username",None)
    email = request.form.get("email",None)
    password = request.form.get("password",None)
    confirm_password = request.form.get("confirm",None)

    if not username or not password or not email or not confirm_password:
        return jsonify(msg="Malformed request: Check if all fields included"),401
    
    if password != confirm_password:
        return jsonify(msg="Password and confirm pasword does not match"),400

    password = bcrypt.generate_password_hash(password)
    u = User(name = username, email = email, password = password)
    try:
        db.session.add(u)
        db.session.commit()
        return jsonify(msg="Account creation successful"),200

    except IntegrityError as e:
        return jsonify(msg="Email or username already exists"),400