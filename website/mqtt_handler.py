from flask_mqtt import Mqtt
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util import Counter
import binascii
import base64

topic = 'test'

class MQTTClient:
    def __init__(self, app):
        self.app = app
        self.mqtt = Mqtt(app)
        self.key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10'
        self.register_event_handlers()


    def register_event_handlers(self):
        @self.mqtt.on_connect()
        def handle_connect(client, userdata, flags, rc):
            print(f'on_connect client: {client}, userdata: {userdata}, flags: {flags}, rc: {rc}')
            self.mqtt.subscribe(topic)

        @self.mqtt.on_message()
        def handle_mqtt_message(client, userdata, message):
            data = dict(
                topic=message.topic,
                payload=message.payload
            )
            print(f'Received message on topic: {data["topic"]} with payload: {data["payload"]}')
            with self.app.app_context():
                rec_data = data['payload']
                print(rec_data)


# def decrypt_data(encrypted_data):
#     cipher = AES.new(key, AES.MODE_ECB)
#     decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
#     return decrypted_data
    # encrypted_data = base64.b64decode(encrypted_data_base64['payload'])
    # iv = encrypted_data[:16]
    # encrypted_message = encrypted_data[16:]
    # cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # try:
    #     decrypted_data = unpad(cipher.decrypt(encrypted_message), AES.block_size)
    # except ValueError:
    #     raise ValueError("Padding is incorrect")
    
    # return decrypted_data.decode('utf-8')
