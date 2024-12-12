from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from datetime import datetime
from . import db
from .models import User, PatientSpecificData, DoctorSpecificData, Bookings
from .handles import handle_create_booking


views = Blueprint('views', __name__)

@views.route("/", methods=["POST", "GET"])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    return render_template('index.html', user=current_user)


@views.route('/booking', methods = ['POST', 'GET'])
@login_required
def booking():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    result = handle_create_booking(request.method, request.form)

    if result == 'GET':
        return render_template('booking.html', user=current_user)
    
    if result is not True:
        flash(result, category='error')
        return render_template('booking.html', user=current_user)
    
    return redirect(url_for('views.home'))

@views.route('/patient-bookings', methods=['POST','GET'])
@login_required
def all_bookings():
    if session['user_type']:
        user_type = session["user_type"]
    else:
        user_type = None

    patients = Patient.query.all()

    patients_with_bookings = [
        {
            'id': patient.id,
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'bookings': sorted(
                patient.bookings,
                key=lambda b: datetime.strptime(f"{b['date']} {b['time']}", "%Y-%m-%d %H:%M")
            )
        }
        for patient in patients if patient.bookings
    ]
    if session["user_type"] != 'doctor':
        flash('Kun læger har adgang til dette', category='error')
        return redirect(url_for('views.home'))
    
    if request.method != 'POST':
        return render_template('all-bookings.html', user=current_user, user_type=user_type, patients=patients_with_bookings)
    
    return render_template('all-bookings.html', user=current_user, user_type=user_type, patients=patients_with_bookings)

@views.route('/patient-bookings/<int:patient_id>')
@login_required
def patient_bookings():
    if session['user_type']:
        user_type = session["user_type"]
    else:
        user_type = None

    if session["user_type"] != 'doctor':
        flash('Kun læger har adgang til dette', category='error')
        return redirect(url_for('views.home'))

    if request.method != 'POST':
        return render_template('patient-bookings.html', user=current_user, user_type=user_type)

    return render_template('patient-bookings.html', user=current_user,)