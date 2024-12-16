from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_session import Session
from .mqtt_handler import MQTTClient

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

    app.config['MQTT_BROKER_URL'] = '74.234.45.30'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_KEEPALIVE'] = 5
    # app.config['MQTT_TLS_ENABLED'] = True

    #MQTT Client
    mqtt_client = MQTTClient(app)

    # topic = 'test'
    # mqtt = Mqtt(app)

    # @mqtt.on_connect()
    # def handle_connect(client, userdata, flags, rc):
    #     print('on_connect client : {} userdata :{} flags :{} rc:{}'.format(client, userdata, flags, rc))
    #     mqtt.subscribe(topic)

    # @mqtt.on_message()
    # def handle_mqtt_message(client, userdata, message):
    #     data = dict(
    #         topic=message.topic,
    #         payload=message.payload.decode()
    #         )
    #     print('Received message on topic: {topic} with payload: {payload}'.format(**data))

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, PatientSpecificData, DoctorSpecificData, Bookings

    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message = "Du skal være logget ind for at få adgang til denne side."


    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))
        return user

    return app