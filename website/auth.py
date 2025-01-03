from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
import os
import hashlib
from .handles import handle_login, handle_patient_register, handle_doctor_register

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('views.home')

    result, user = handle_login(request.method, request.form)

    if result == 'GET':
        return render_template('login.html', user=current_user)

    if result is not True:
        flash(result, category='error')
        return render_template('login.html', user=current_user)
    
    login_user(user, remember=True)

    return redirect(url_for('views.home'))

@auth.route("/lav-bruger", methods=["POST", "GET"])
def patient_register():
    if current_user.is_authenticated:
        return redirect('views.home')
    
    result, patient = handle_patient_register(request.method, request.form)

    if result == 'GET':
        return render_template('patient-register.html', user=current_user)
    
    if result is not True:
        flash(result, category='error')
        return render_template('patient-register.html', user=current_user)

    flash('Bruger lavet!', category='success')
    login_user(patient, remember=True)

    return redirect(url_for('views.home'))


@auth.route("/læge-lav-bruger", methods=["POST", "GET"])
def doctor_register():
    if current_user.is_authenticated:
        return redirect('views.home')
    
    result, doctor = handle_doctor_register(request.method, request.form)

    if result == 'GET':
        return render_template('doctor-register.html', user=current_user)
    
    if result is not True:
        flash(result, category='error')
        return render_template('doctor-register.html', user=current_user)
    
    flash('Læge bruger lavet!', category='success')
    login_user(doctor, remember=True)

    return redirect(url_for('views.home'))


@auth.route("/log-ud")
@login_required
def logout():
    logout_user()
    flash('Logget ud!', category='success')
    return redirect(url_for('auth.login'))
