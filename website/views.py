from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from datetime import datetime
from . import db
from .models import User, PatientSpecificData, DoctorSpecificData, Bookings
from .handles import handle_create_booking, handle_all_bookings, handle_patient_details
from .functions import get_available_times


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
    
    flash('Booking lavet!', category='success')
    return redirect(url_for('views.home'))

@views.route('/update_available_times', methods=['GET'])
def update_available_times():
    selected_date = request.args.get('date')

    available_dates = get_available_times(selected_date)
    return available_dates

@views.route('/patient-bookings', methods=['POST', 'GET'])
@login_required
def all_bookings():
    result, grouped_bookings = handle_all_bookings(request.method, request.form)

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