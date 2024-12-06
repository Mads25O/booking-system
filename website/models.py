from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Patient(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    hashed_cpr_number = db.Column(db.String(64), unique=True)
    cpr_salt = db.Column(db.String(32))
    hashed_password = db.Column(db.String(128))
    password_salt = db.Column(db.String(32))
    phone = db.Column(db.Integer)
    email = db.Column(db.String(150), unique=True)


class Doctor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    password_salt = db.Column(db.String(32))
    phone = db.Column(db.Integer)
    email = db.Column(db.String(150), unique=True)
