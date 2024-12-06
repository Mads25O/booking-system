from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from .models import Patient, Doctor
from . import db
import os
import hashlib

auth = Blueprint('auth', __name__)

def generate_hash(cpr_number, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()
    return hashlib.sha256((cpr_number + salt).encode()).hexdigest(), salt

def check_cpr_exists(cpr_number):
    patient = Patient.query.first()
    if patient:
        hashed_cpr, _ = generate_hash(cpr_number, patient.cpr_salt)
        if hashed_cpr == patient.hashed_cpr_number:
            return True, patient
    return False, None

def check_email_exists(email):
    return Patient.query.filter_by(email=email).first() is not None


@auth.route("/login", methods=["POST", "GET"])
def patient_login():
    if request.method != 'POST':
        return render_template('patient-login.html')
    
    cpr_number_form = request.form.get("cpr_number")
    password_form = request.form.get("password")

    cpr_exists, patient = check_cpr_exists(cpr_number_form)
    print(patient)
    if cpr_exists != False and patient != None:
        hashed_password, _ = generate_hash(password_form, patient.password_salt)
        if hashed_password == patient.hashed_password:
            print("logget ind")

        session["user"] = patient.id
    return redirect(url_for("auth.user"))



@auth.route("/user")
def user():
    if "user" in session:
        user = session["user"]
    else:
        return redirect(url_for("patient_login"))
    return f"<h1>{user}</h1>"
    
@auth.route("/læge-login")
def doctor_login():
    if request.method == 'POST':
        pass
    else: 
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
    if cpr_exists:
        flash('CPR-nummeret er allerede i systemet', category='error')
    elif password_form != password_form_confirm:
        flash('Adgangskoden stemmer ikke overens', category='error')
    elif email_form != email_form_confirm:
        flash('E-mail adressen stemmer ikke overens', category='error')
    elif check_email_exists(email_form):
        flash('E-mail adressen er allerede i systemet', category='error')
    elif len(password_form) < 10:
        flash('Adgangskoden er for kort', category='error')
    
    # elif password != speciale_tegn:
    #   fejl
    # elif password != ikke_stort_bogstav:
    #   fejl

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
        # login_user(new_patient, remember=True)

        flash('Bruger lavet!', category='success')
        return redirect(url_for('views.home'))

    return render_template('patient-register.html')
    
    # new_patient = Patient(cpr)

@auth.route("/læge-lav-bruger")
def doctor_register():
    return render_template('doctor-register.html')



@auth.route("/log-ud")
def logout():
    pass