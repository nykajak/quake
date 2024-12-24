from api import app,db
from api.models import *
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

@app.get("/")
def home():
    return "Hello world!"

@app.post("/login")
def login():
    username = request.form.get("username",None)
    password = request.form.get("password",None)
    
    res = User.query.filter(User.name == username, User.password == password).scalar()
    print(res)
    if res:
        return "Logged in!"

    return "Unable to login!"

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