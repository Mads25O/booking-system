from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from datetime import datetime
from . import db
from .models import User, PatientSpecificData, DoctorSpecificData, Bookings


views = Blueprint('views', __name__)

@views.route("/", methods=["POST", "GET"])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    return render_template('index.html', user=current_user)


@views.route('/booking', methods = ['POST', 'GET'])
@login_required
def booking():
    if session['user_type']:
        user_type = session["user_type"]
    else:
        user_type = None

    if request.method != 'POST':
        return render_template('booking.html', user=current_user, user_type=user_type)
    
    user_id = session.get("user").split(':')[1]
    patient = Patient.query.get(user_id)
    bookings = Bookings.query.filter_by(user_id=user_id).all()

    if not patient:
        flash('Bruger ikke fundet', category='error')
        return redirect(url_for('auth.login'))

    booking_date = request.form.get('date')
    booking_time = request.form.get('time')

    new_booking = {
        'user_id': user_id,
        'date': booking_date,
        'time': booking_time,
        'created_at': datetime.now().isoformat()
    }

    bookings.bookings = bookings.bookings or []
    bookings.bookings.append(new_booking)

    try:
        db.session.add(bookings)
        db.session.commit()
        flash('Booking oprettet!', category='success')
    except Exception as e:
        flash(f'Fejl {e}')
    

    return render_template('booking.html', user=current_user, user_type=user_type)

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
def patient_bookings(patient_id):
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