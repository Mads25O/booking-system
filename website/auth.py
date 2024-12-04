from flask import Flask, Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route("/login")
def login():
    return render_template('login.html')

@auth.route("/sign-up")
def sign_up():
    return render_template('sign-up.html')

@auth.route("/logout")
def logout():
    pass