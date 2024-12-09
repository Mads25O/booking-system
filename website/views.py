from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from datetime import datetime
from . import db
from .models import Patient


views = Blueprint('views', __name__)

@views.route("/", methods=["POST", "GET"])
def home():
    if request.method != 'POST':
        return render_template('index.html')
    
    if request.form.get('patient_button'):
        return redirect(url_for('auth.patient_login'))
    elif request.form.get('doctor_button'):
        return redirect(url_for('auth.doctor_login'))

    return render_template('index.html')

@views.route('/logged')
@login_required
def logged():
    return render_template('logged-in.html')

@views.route('/patient-side', methods = ['POST', 'GET'])
@login_required
def patient_home():
    if request.method != 'POST':
        return render_template('patient-side.html')
    
    if request.form.get('billeddiagnostik'):
        return redirect(url_for('views.booking'))

    return render_template('patient-side.html')

@views.route('/booking', methods = ['POST', 'GET'])
@login_required
def booking():
    if request.method != 'POST':
        return render_template('booking.html')
    
    user_id = session.get("user").split(':')[1]
    print(user_id)
    patient = Patient.query.get(user_id)

    if not patient:
        flash('Bruger ikke fundet', category='error')
        return redirect(url_for('auth.patient_login'))

    booking_date = request.form.get('date')
    booking_time = request.form.get('time')

    new_booking = {
        'date': booking_date,
        'time': booking_time,
        'created_at': datetime.now().isoformat()
    }

    user_bookings = patient.bookings or []
    user_bookings.append(new_booking)
    patient.bookings = user_bookings

    db.session.commit()
    
    flash('Booking oprettet!', category='success')

    return render_template('booking.html')

@views.route('/patient-bookings', methods=['POST','GET'])
@login_required
def all_bookings():
    if session["user_type"] != 'doctor':
        flash('Kun læger har adgang til dette', category='error')
        return redirect(url_for('views.patient_home'))
    
    if request.method != 'POST':
        print(session["user_type"])
        print(type(session["user_type"]))
        return render_template('all-bookings.html')
    
    return render_template('all-bookings.html')

@views.route('/patient-bookings/<int:patient_id>')
@login_required
def patient_bookings(patient_id):
    if session["user_type"] != 'doctor':
        flash('Kun læger har adgang til dette', category='error')
        return redirect(url_for('views.patient_home'))
    
    if request.method != 'POST':
        return render_template('patient-bookings.html')

    return render_template('patient-bookings.html')