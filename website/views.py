from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route("/", methods=["POST", "GET"])
def home():
    if request.method != 'POST':
        return render_template('index.html')
    
    if request.form.get('patient_button'):
        print('meow')
        return redirect(url_for('auth.patient_login'))
    elif request.form.get('doctor_button'):
        return redirect(url_for('auth.doctor_login'))

    return render_template('index.html')

@views.route("/yt-website")
def yt_website():
    return render_template('yt-website.html')

@views.route('/logged')
@login_required
def logged():
    return render_template('logged-in.html')