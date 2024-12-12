from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from sqlalchemy.orm import joinedload
from .models import User, PatientSpecificData, DoctorSpecificData, Bookings
from . import db
from .functions import generate_hash, check_cpr_exists, check_user_exists, validate_password
import os
import hashlib
from datetime import datetime

def handle_login(method, form_data):
    if method != 'POST':
        return 'GET', None
    
    if form_data.get('patient_login'):
        cpr_number_form = form_data.get("cpr_number")
        password_form = form_data.get("password")

        cpr_exists, patient = check_cpr_exists(cpr_number_form)
        if cpr_exists:
            user = User.query.filter_by(id=patient.user_id).first()
            hashed_password, _ = generate_hash(password_form, user.password_salt)
            if hashed_password == user.hashed_password:
                return True, user
            else:
                return 'Forkert kode', None
        else:
            return 'CPR er ikke i systemet', None

    if form_data.get('doctor_login'):
        email_form = form_data.get("email_name")
        password_form = form_data.get("password_name")

        email_exists, doctor = check_user_exists(email_form)
        if email_exists:
            hashed_password, _ = generate_hash(password_form, doctor.password_salt)
            if hashed_password == doctor.hashed_password:
                return True, doctor
            else:
                return 'Forkert kode', None
        else:
            return 'E-mail er ikke i systemet', None
    

def handle_patient_register(method, form_data):
    if method != 'POST':
        return 'GET', None
    
    cpr_number_form = form_data.get('cpr_number_name')
    first_name_form = form_data.get('first_name_name')
    last_name_form = form_data.get('last_name_name')
    password_form = form_data.get('password_name')
    password_form_confirm = form_data.get('password_name_confirm')
    email_form = form_data.get('email_name')
    email_form_confirm = form_data.get('email_name_confirm')
    phone_form = form_data.get('phone_name')

    cpr_exists, _ = check_cpr_exists(cpr_number_form)
    email_exists, _ = check_user_exists(email_form)

    if cpr_exists:
        return 'CPR-nummeret er allerede i systemet', None
    elif password_form != password_form_confirm:
        return 'Adgangskoderne stemmer ikke overens', None
    elif email_form != email_form_confirm:
        return 'E-mail adressen stemmer ikke overens', None
    elif email_exists:
        return 'E-mail adressen er allerede i systemet', None
    elif len(password_form) < 10:
        return 'Adgangskoden er for kort', None
    # elif password != speciale_tegn:
    #   kode for nem
    # elif password != ikke_stort_bogstav:
    #   kode for nem
    else:
        hashed_cpr, cpr_salt = generate_hash(cpr_number_form)
        hashed_password, password_salt = generate_hash(password_form)

        new_patient = User(
            first_name=first_name_form,
            last_name=last_name_form,
            hashed_password=hashed_password,
            password_salt=password_salt,
            phone=phone_form,
            role='patient'
        )

        db.session.add(new_patient)
        db.session.commit()
        
        new_patient_data = PatientSpecificData(
            user_id=new_patient.id,
            hashed_cpr=hashed_cpr,
            cpr_salt=cpr_salt,
            email=email_form
        )
        
        db.session.add(new_patient_data)
        db.session.commit()

        return True, new_patient

def handle_doctor_register(method, form_data):
    if method != 'POST':
        return 'GET', None
    
    first_name_form = form_data.get('first_name_name')
    last_name_form = form_data.get('last_name_name')
    username_form = form_data.get('username_name')
    password_form = form_data.get('password_name')
    password_form_confirm = form_data.get('password_name_confirm')
    phone_form = form_data.get('phone_name')

    username_exists, _ = check_user_exists(username_form)
    if username_exists:
        return 'Brugernavn findes allerede', None
    elif password_form != password_form_confirm:
        return 'Adgangskoden stemmer ikke overens', None
    elif len(password_form) < 10:
        return 'Adgangskoden er for kort', None
    
    # elif password != speciale_tegn:
    #   kode for nem
    # elif password != ikke_stort_bogstav:
    #   kode for nem

    else:
        hashed_password, password_salt = generate_hash(password_form)

        new_doctor = User(
            first_name=first_name_form,
            last_name=last_name_form,
            hashed_password=hashed_password,
            password_salt=password_salt,
            phone=phone_form,
            role='doctor'
        )
        
        db.session.add(new_doctor)
        db.session.commit()

        new_doctor_data = DoctorSpecificData(
            user_id=new_doctor.id,
            username=username_form
        )

        db.session.add(new_doctor_data)
        db.session.commit()

        return True, new_doctor

def handle_create_booking(method, form_data):
    if method != 'POST':
        return 'GET'
    
    patient = User.query.get(current_user.id)

    if not patient:
        return 'Bruger ikke fundet', None

    booking_date = request.form.get('date')
    booking_time = request.form.get('time')

    patient_id = PatientSpecificData.query.filter_by(user_id=current_user.id).first()

    new_booking = Bookings(
        user_id=current_user.id,
        patient_id=patient_id.user_id,
        date=booking_date,
        time=booking_time,
        created_at=datetime.now().isoformat()
    )

    try:
        db.session.add(new_booking)
        db.session.commit()
    except Exception as e:
        return f'Fejl {e}. Prøv igen'
    
    return True

def handle_all_bookings(method, form_data):
    if method == 'POST':
        patient_details = form_data.get('patient_booking')
        print(f"Patient ID modtaget: {patient_details}")
        return patient_details, None

    bookings = Bookings.query.join(Bookings.patient).order_by(Bookings.date, Bookings.time).all()

    return True, bookings

def handle_patient_details(method, form_data, user):
    patient_id = user.id
    patient_bookings = Bookings.query.filter_by(user_id=patient_id).all()
    patient_details = PatientSpecificData.query.filter_by(user_id=patient_id).all()

    if method == 'POST':
        if form_data.get('patient-details-button'):

            
            email = form_data.get('email')
            phone = form_data.get('phone')
            old_password = form_data.get('old_password')
            new_password = form_data.get('new_password')
            new_password_confirm = form_data.get('new_password_confirm')


            if email and email.strip():
                email_exists, _ = check_user_exists(email)
                if email_exists:
                    print('Email findes')
                    return 'Email er allerede i systemet.', patient_bookings, patient_details
                else:
                    patient_details[0].email = email
                    print(email)
                    print(patient_details[0].email)
            
            if old_password and old_password.strip():
                hashed_password, _ = generate_hash(old_password, user.password_salt)
                if hashed_password == user.hashed_password:
                    print(f"Hashed new password: {hashed_password}, Password salt: {user.password_salt}")
                    user.phone = phone

                else:
                    print('Forkert kode')
                    return 'Forkert kode', patient_bookings, patient_details

            if new_password and new_password.strip():
                if len(new_password) < 10:
                    print('Kode for kort')
                    return 'Adgangskoden er for kort', patient_bookings, patient_details
                elif new_password != new_password_confirm:
                    print('Kode stemmer ikke overens')
                    return 'Adgangskoden stemmer ikke overens', patient_bookings, patient_details   
                else:
                    user.password = new_password

            if phone and phone.strip():
                user.phone = phone

            try:
                db.session.commit()
            except Exception as e:
                print(f"Fejl under database commit: {e}")
                return f'Fejl: {e}', patient_bookings, patient_details
                

    return True, patient_bookings, patient_details