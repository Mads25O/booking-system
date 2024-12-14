from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from sqlalchemy.orm import joinedload
from .models import User, PatientSpecificData, DoctorSpecificData, Bookings
from . import db
import os
import hashlib
from datetime import datetime, timedelta

def generate_hash(unhashed_value, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()
    return hashlib.sha256((unhashed_value + salt).encode()).hexdigest(), salt

def check_cpr_exists(cpr_number):
    patients = PatientSpecificData.query.all()
    for patient in patients:
        hashed_cpr, _ = generate_hash(cpr_number, patient.cpr_salt)
        if hashed_cpr == patient.hashed_cpr:
            return True, patient
    return False, None

def check_user_exists(identity):
    patient = PatientSpecificData.query.filter_by(email=identity).first()

    if patient:
        user = User.query.get(patient.user_id)
        return True, user
    
    doctor = DoctorSpecificData.query.filter_by(username=identity).first()

    if doctor:
        user = User.query.get(doctor.user_id)
        return True, user
    
    return False, None

def validate_password(password, confirm_password):
    if len(password) < 10:
        return "Adgangskoden skal være mindst 10 tegn lang."
    
    if not any(char.isupper() for char in password):
        return "Adgangskoden skal indeholde mindst ét stort bogstav."
    
    if not any(char.islower() for char in password):
        return "Adgangskoden skal indeholde mindst ét lille bogstav."
    
    if not any(char.isdigit() for char in password):
        return "Adgangskoden skal indeholde mindst ét tal."
    
    if not any(char in "!@#$%^&*()-_=+[]{};:'\"|\\,.<>?/`~" for char in password):
        return "Adgangskoden skal indeholde mindst ét specialtegn."

    if confirm_password is not None and password != confirm_password:
        return "Adgangskoden matcher ikke bekræftelsen."
    
    return True

# def generate_time_slots(start, end, existing_bookings=None, interval_minutes=30):
#     slots = []
#     current_time = start
#     while current_time <= end:
        
#         # slots.append(current_time.strftime('%H:%M'))
#         # current_time += timedelta(minutes=interval_minutes)
#         time_str = current_time.strftime('%H:%M')

#         if existing_bookings and time_str not in existing_bookings:
#             slots.append(time_str)
#         elif not existing_bookings:
#             slots.append(time_str)

#         current_time += timedelta(minutes=interval_minutes)

#     print(f"Existing bookings for date: {existing_bookings}")
#     print(f"Generated slots: {slots}")
#     # if not slots:
#     #     return "Alt er booket"
    
#     return slots

def get_available_times(date):
    existing_bookings = Bookings.query.filter_by(date=date).all()
    
    all_times = [f"{hour:02d}:{minute:02d}" for hour in range(8, 17) for minute in [0, 30]]
    booked_times = [booking.time for booking in existing_bookings]

    available_times = [time for time in all_times if time not in booked_times]

    if not available_times:
        return "Alt er booket i dag", []
    
    return available_times