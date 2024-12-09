from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_session import Session

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "SECRET"
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Patient, Doctor

    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'views.home'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id_with_prefix):
        if not id_with_prefix or ':' not in id_with_prefix:
            return None
        
        try:
            user_type, id = id_with_prefix.split(":")
            id = int(id)
        except ValueError:
            return None
        
        if user_type == 'patient':
            return Patient.query.get(int(id))
        elif user_type == 'doctor':
            return Doctor.query.get(int(id))
        return None

    return app