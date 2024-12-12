from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    hashed_password = db.Column(db.String(128))
    password_salt = db.Column(db.String(32))
    role = db.Column(db.String(10))
    phone = db.Column(db.Integer)

    bookings = db.relationship('Bookings', back_populates='user')

    def is_patient(self):
        return self.role == 'patient'

    def is_doctor(self):
        return self.role == 'doctor'

class PatientSpecificData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    hashed_cpr = db.Column(db.String(64))
    cpr_salt = db.Column(db.String(32))
    email = db.Column(db.String(150), unique=True)
    bookings = db.relationship('Bookings', back_populates='patient')

class DoctorSpecificData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    username = db.Column(db.String(16))

class Bookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_specific_data.id'))
    date = db.Column(db.String(100))
    time = db.Column(db.String(100))
    created_at = db.Column(db.String(100))

    user = db.relationship('User', back_populates='bookings', foreign_keys=[user_id])
    patient = db.relationship('PatientSpecificData', back_populates='bookings', foreign_keys=[patient_id])