from api import app,db
from api.models import *
from flask import request, jsonify
from flask_jwt_extended import create_access_token,jwt_required,set_access_cookies,unset_jwt_cookies
from sqlalchemy.exc import IntegrityError

@app.get("/")
def home():
    return jsonify(msg="Hello world!")


@app.post("/login")
def login():
    username = request.form.get("username",None)
    password = request.form.get("password",None)
    
    res = User.query.filter(User.name == username, User.password == password).scalar()

    if res:
        response = jsonify(msg="Login success!")
        access_token = create_access_token(identity=username)
        set_access_cookies(response,access_token)
        return response

    return jsonify(msg="Login failed!")

@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@app.post("/register")
def register():
    username = request.form.get("username",None)
    email = request.form.get("email",None)
    password = request.form.get("password",None)
    confirm_password = request.form.get("confirm",None)
    
    if password != confirm_password:
        return "Account creation failed!"

    u = User(name = username, email = email, password = password)
    try:
        db.session.add(u)
        db.session.commit()
        return "Account created!"

    except IntegrityError as e:
        return "Account creation failed!"

@app.get("/all")
@jwt_required()
def all():
    l = User.query.filter()
    res = []
    for x in l:
        res.append(
            {
                "name" : x.name,
                "password" : x.password,
            }
        )
    return jsonify(payload = res)