from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User, PatientSpecificData
from .handles import handle_create_booking, handle_all_bookings, handle_patient_details, handle_doctor_details
from .functions import get_available_times, encrypt_data


views = Blueprint('views', __name__)

@views.route("/", methods=["POST", "GET"])
@login_required
def home():
    if current_user.role == 'patient':
        patient_details = PatientSpecificData.query.filter_by(user_id=current_user.id).first()
        reference = patient_details.reference
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
    if current_user.role != 'doctor':
        flash('Denne side er kun for læger!', category='error')
        return redirect(url_for('views.home'))
    grouped_bookings = handle_all_bookings(request.method, request.form)

    return render_template('all-bookings.html', user=current_user, bookings=grouped_bookings)

@views.route('/patient-detaljer/<int:patient_id>', methods=['POST', 'GET'])
@login_required
def patient_details(patient_id):
    if patient_id != current_user.id and current_user.role != 'doctor':
        flash(f'Du må ikke kigge på denne brugers oplysninger!', category='error')
        return redirect(url_for('views.home'))
    
    key = b'\xb1\x84\xa6\xe8\x93Jk\xdb\xb5|\xf3{\xa4\x98\x07G#w!\x82\xe8\xb3c\x11$\xeb\x10\x15\xaa?W('
    iv = b'\xc1\xd6\n\xd3v\xdae$\xb2\xbd\x17\x8e\xe1\xc4\x1e\xd9'
    print(current_user.uid)
    if current_user.uid != None:
        user_uid = encrypt_data(current_user.uid, key, iv)
        print(user_uid)
    else:
        user_uid = ''
    
    patient = User.query.filter_by(id=patient_id).first()
    result, patient_bookings, patient_details = handle_patient_details(request.method, request.form, patient)

    if result is not True:
        flash(result, category='error')

    if result is True:
        flash('Success!', category='success')

    return render_template(
        'patient-details.html',
        user=current_user, 
        patient=patient, 
        patient_bookings=patient_bookings,
        patient_details=patient_details,
        user_uid=user_uid)

@views.route('/læge-detaljer/<int:doctor_id>', methods=['POST', 'GET'])
@login_required
def doctor_details(doctor_id):
    if doctor_id != current_user.id or current_user.role != 'doctor':
        flash(f'Du må ikke kigge på denne brugers oplysninger!', category='error')
        return redirect(url_for('views.home'))
    
    key = b'\xb1\x84\xa6\xe8\x93Jk\xdb\xb5|\xf3{\xa4\x98\x07G#w!\x82\xe8\xb3c\x11$\xeb\x10\x15\xaa?W('
    iv = b'\xc1\xd6\n\xd3v\xdae$\xb2\xbd\x17\x8e\xe1\xc4\x1e\xd9'

    if current_user.uid != None:
        user_uid = encrypt_data(current_user.uid, key, iv)
    else:
        user_uid = ''

    result = handle_doctor_details(request.method, request.form, current_user)

    if result == 'GET':
        return render_template('doctor-details.html', user=current_user)

    if result is not True:
        flash(result, category='error')

    if result is True:
        flash('Success!', category='success')
    
    return render_template('doctor-details.html', user=current_user, user_uid=user_uid)

@views.route('/alle-patienter', methods=['POST', 'GET'])
@login_required
def all_patients():
    patients = User.query.filter_by(role='patient').all()
    return render_template('all-patients.html', user=current_user, patients=patients)
