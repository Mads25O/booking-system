from flask import Flask, Blueprint, render_template

views = Blueprint('views', __name__)

@views.route("/")
def home():
    return render_template('index.html')

@views.route("/yt-website")
def yt_website():
    return render_template('yt-website.html')