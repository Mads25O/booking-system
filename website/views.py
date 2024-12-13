from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from datetime import datetime
from . import db
from .models import User, PatientSpecificData, DoctorSpecificData, Bookings
from .handles import handle_create_booking, handle_all_bookings, handle_patient_details
from .functions import get_available_times


views = Blueprint('views', __name__)

@views.route("/", methods=["POST", "GET"])
@login_required
def home():
    user_id = current_user.id
    if current_user.role == 'patient':
        patient_details = PatientSpecificData.query.filter_by(user_id=user_id).first()
        reference = patient_details.reference
        print(reference)
    else:
        reference = None

    return render_template('index.html', user=current_user, reference=reference)


@views.route('/booking', methods = ['POST', 'GET'])
@login_required
def booking():
    result = handle_create_booking(request.method, request.form)

    if result == 'GET':
        return render_template('booking.html', user=current_user)
    
    if result is not True:
        flash(result, category='error')
        return render_template('booking.html', user=current_user)
    
    flash('Booking lavet!', category='success')
    return redirect(url_for('views.home'))

@views.route('/update_available_times', methods=['GET'])
@login_required
def update_available_times():
    selected_date = request.args.get('date')

    available_dates = get_available_times(selected_date)
    return available_dates

@views.route('/patient-bookings', methods=['POST', 'GET'])
@login_required
def all_bookings():
    grouped_bookings = handle_all_bookings(request.method, request.form)
    print(grouped_bookings)

    return render_template('all-bookings.html', user=current_user, bookings=grouped_bookings)

@views.route('/patient-detaljer/<int:patient_id>', methods=['POST', 'GET'])
@login_required
def patient_details(patient_id):


    patient = User.query.filter_by(id=patient_id).first()
    result, patient_bookings, patient_details = handle_patient_details(request.method, request.form, patient)

    if result is not True:
        flash(result, category='error')


    return render_template(
        'patient-details.html',
        user=current_user, 
        patient=patient, 
        patient_bookings=patient_bookings,
        patient_details=patient_details)

@views.route('/alle-patienter', methods=['POST', 'GET'])
@login_required
def all_patients():
    patients = User.query.filter_by(role='patient').all()
    return render_template('all-patients.html', user=current_user, patients=patients)