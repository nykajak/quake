from api.database import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(40),unique = True)
    email = db.Column(db.String(128),unique = True)
    password = db.Column(db.String(64))