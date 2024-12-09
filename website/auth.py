from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from .models import Patient, Doctor
from . import db
import os
import hashlib

auth = Blueprint('auth', __name__)

def generate_hash(unhashed_value, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()
    return hashlib.sha256((unhashed_value + salt).encode()).hexdigest(), salt

def check_cpr_exists(cpr_number):
    patients = Patient.query.all()
    for patient in patients:
        hashed_cpr, _ = generate_hash(cpr_number, patient.cpr_salt)
        if hashed_cpr == patient.hashed_cpr_number:
            return True, patient
    return False, None

def check_email_exists(email, user_type):
    if user_type == 'patient':
        users = Patient.query.all()
    if user_type == 'doctor':
        users = Doctor.query.all()

    for user in users:
        if user.email == email:
            return True, user
    return False, None


@auth.route("/login", methods=["POST", "GET"])
def patient_login():
    if request.method != 'POST':
        return render_template('patient-login.html')
    
    cpr_number_form = request.form.get("cpr_number")
    password_form = request.form.get("password")

    cpr_exists, patient = check_cpr_exists(cpr_number_form)
    if cpr_exists != False and patient != None:
        hashed_password, _ = generate_hash(password_form, patient.password_salt)
        if hashed_password == patient.hashed_password:
            login_user(patient, remember=True)

            session["user"] = f'patient:{patient.id}'
            session["user_type"] = f'patient'

            return redirect(url_for("views.patient_home"))
        else:
            flash('Forkert kode', category='error')
    else:
        flash('CPR er ikke i systemet', category='error')
    
    return render_template('patient-login.html')

    
@auth.route("/læge-login", methods=["POST", "GET"])
def doctor_login():
    if request.method != 'POST':
        return render_template('doctor-login.html')
    
    email_form = request.form.get("email_name")
    password_form = request.form.get("password_name")

    email_exists, doctor = check_email_exists(email_form, 'doctor')
    if email_exists:
        hashed_password, _ = generate_hash(password_form, doctor.password_salt)
        if hashed_password == doctor.hashed_password:
            login_user(doctor, remember=True)

            session["user"] = f'doctor:{doctor.id}'
            session["user_type"] = 'patient'
            return redirect(url_for("views.logged"))
        else:
            flash('Forkert kode', category='error')
    else:
        flash('E-mail ikke i systemet', category='error')
   
    
    return render_template('doctor-login.html')
        


@auth.route("/lav-bruger", methods=["POST", "GET"])
def patient_register():
    if request.method != 'POST':
        return render_template('patient-register.html')
    
    cpr_number_form = request.form.get('cpr_number_name')
    first_name_form = request.form.get('first_name_name')
    last_name_form = request.form.get('last_name_name')
    password_form = request.form.get('password_name')
    password_form_confirm = request.form.get('password_name_confirm')
    email_form = request.form.get('email_name')
    email_form_confirm = request.form.get('email_name_confirm')
    phone_form = request.form.get('phone_name')

    # cpr_number = Patient.query.filter_by(cpr_number=cpr_number_form).first()
    
    cpr_exists, _ = check_cpr_exists(cpr_number_form)
    email_exists, _ = check_email_exists(email_form, 'patient')

    if cpr_exists:
        flash('CPR-nummeret er allerede i systemet', category='error')
    elif password_form != password_form_confirm:
        flash('Adgangskoden stemmer ikke overens', category='error')
    elif email_form != email_form_confirm:
        flash('E-mail adressen stemmer ikke overens', category='error')
    elif email_exists:
        flash('E-mail adressen er allerede i systemet', category='error')
    elif len(password_form) < 10:
        flash('Adgangskoden er for kort', category='error')
    
    # elif password != speciale_tegn:
    #   kode for nem
    # elif password != ikke_stort_bogstav:
    #   kode for nem

    else:
        hashed_cpr, cpr_salt = generate_hash(cpr_number_form)
        hashed_password, password_salt = generate_hash(password_form)

        new_patient = Patient(hashed_cpr_number=hashed_cpr,
                                cpr_salt=cpr_salt,
                                first_name=first_name_form,
                                last_name=last_name_form,
                                hashed_password=hashed_password,
                                password_salt=password_salt,
                                email=email_form,
                                phone=phone_form
                                )
        
        db.session.add(new_patient)
        db.session.commit()
        login_user(new_patient, remember=True)

        session["user"] = f'patient:{new_patient.id}'
        session["user_type"] = f'patient'

        flash('Bruger lavet!', category='success')
        return redirect(url_for('views.patient_home'))

    return render_template('patient-register.html')

@auth.route("/læge-lav-bruger", methods=["POST", "GET"])
def doctor_register():
    if request.method != 'POST':
        return render_template('doctor-register.html')
    
    first_name_form = request.form.get('first_name_name')
    last_name_form = request.form.get('last_name_name')
    password_form = request.form.get('password_name')
    password_form_confirm = request.form.get('password_name_confirm')
    email_form = request.form.get('email_name')
    email_form_confirm = request.form.get('email_name_confirm')
    phone_form = request.form.get('phone_name')

    email_exists, _ = check_email_exists(email_form, 'doctor')


    if password_form != password_form_confirm:
        flash('Adgangskoden stemmer ikke overens', category='error')
    elif email_form != email_form_confirm:
        flash('E-mail adressen stemmer ikke overens', category='error')
    elif email_exists:
        flash('E-mail adressen er allerede i systemet', category='error')
    elif len(password_form) < 10:
        flash('Adgangskoden er for kort', category='error')
    
    # elif password != speciale_tegn:
    #   kode for nem
    # elif password != ikke_stort_bogstav:
    #   kode for nem

    else:
        hashed_password, password_salt = generate_hash(password_form)

        new_doctor = Doctor(first_name=first_name_form,
                                last_name=last_name_form,
                                hashed_password=hashed_password,
                                password_salt=password_salt,
                                email=email_form,
                                phone=phone_form
                                )
        
        db.session.add(new_doctor)
        db.session.commit()
        login_user(new_doctor, remember=True)

        session["user"] = f'doctor:{new_doctor.id}'
        session["user_type"] = f'doctor'

        flash('Læge bruger lavet!', category='success')
        return redirect(url_for('views.logged'))

    return render_template('doctor-register.html')



@auth.route("/log-ud")
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))