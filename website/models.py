from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Patient(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    hashed_cpr_number = db.Column(db.String(64))
    cpr_salt = db.Column(db.String(32))
    hashed_password = db.Column(db.String(128))
    password_salt = db.Column(db.String(32))
    phone = db.Column(db.Integer)
    email = db.Column(db.String(150), unique=True)
    bookings = db.relationship('Bookings')
    

    # Flask automatisk returnere id, men fordi der er to typer users i dette system, skal funktionen selv defineres.
    def get_id(self):
        return f'patient:{self.id}'


class Doctor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    hashed_password = db.Column(db.String(128))
    password_salt = db.Column(db.String(32))
    phone = db.Column(db.Integer)
    email = db.Column(db.String(150), unique=True)
    
    def get_id(self):
        return f'doctor:{self.id}'

class Bookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookings = db.Column(db.JSON, default=list)
    user_id = db.Column(db.Integer, db.ForeignKey('patient.id'))