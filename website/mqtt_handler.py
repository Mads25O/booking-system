from flask_mqtt import Mqtt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util import Counter
import binascii
import base64
import time

class MQTTClient:
    def __init__(self, app):
        self.app = app
        self.mqtt = Mqtt(app)
        self.topic = 'flask/mqtt/test'
        self.username = 'flask'
        self.password = 'FkwMgxLr5QFv'
        self.key = b'\xb1\x84\xa6\xe8\x93Jk\xdb\xb5|\xf3{\xa4\x98\x07G#w!\x82\xe8\xb3c\x11$\xeb\x10\x15\xaa?W('
        self.iv = b'\xc1\xd6\n\xd3v\xdae$\xb2\xbd\x17\x8e\xe1\xc4\x1e\xd9'
        self.processed_messages = set()
        self.register_event_handlers()
        

    def register_event_handlers(self):
        @self.mqtt.on_connect()
        def handle_connect(client, userdata, flags, rc):
            print(f'on_connect client: {client}, userdata: {userdata}, flags: {flags}, rc: {rc}')
            client.username_pw_set(self.username, self.password)
            self.mqtt.subscribe(self.topic, qos=1)

        @self.mqtt.on_message()
        def handle_mqtt_message(client, userdata, message):
            data = dict(
                topic=message.topic,
                payload=message.payload
            )
            
            print(f'Received message on topic: {data["topic"]} with payload: {data["payload"]}')
            data = data["payload"]
            with self.app.app_context():
                # print('hell yeah')
                # print(len(data))
                print(f"Received encrypted data: {binascii.hexlify(data)}")
                if data in self.processed_messages:
                    # print('duplicateddddd')
                    return None
                self.processed_messages.add(data)
                self.eval_data(data)
        

        @self.mqtt.on_publish()
        def handle_publish(client, userdata, mid):
            print(f'Message with mid {mid} published successfully.')
            # Kontroller for dubletter eller fejl
            if mid in self.processed_messages:
                print(f'Duplicate message with mid {mid}, ignoring.')
            else:
                self.processed_messages.add(mid)
                print(f'Published message with mid {mid}.')

    def encrypt_data(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted_msg = cipher.encrypt(pad(data, 16))
        return encrypted_msg

    def decrypt_data(self, encrypted_data):
        try:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            decrypted = cipher.decrypt(encrypted_data)
            # print(f'Decrypted: {decrypted}')
            decrypted_data = unpad(decrypted, AES.block_size)  # Fjern padding
            print(f'Decrypted_data: {decrypted_data}')
            return decrypted_data.decode('utf-8')
    
        except (ValueError, KeyError) as e:
            # print(f"Error during decryption or unpadding: {e}")
            return None

    def eval_data(self, data):
        from .models import User
        # print('eval data starter')

        decrypted_data = self.decrypt_data(data)
        # print(f'Decrypted_data: {decrypted_data}')
        # print(f'Decrypted_data type_: {type(decrypted_data)}')
        try:
            split_decrypted_data = decrypted_data.split(':')
        except:
            return None
        
        print(split_decrypted_data)

        if split_decrypted_data[0] == 'ESP':
            print('ESP')
        else:
            print('NOESP')
            return None
        
        user = User.query.filter_by(first_name=decrypted_data).first()

        if user:
            response_msg = 'FLASK:TRUE:TIME'.encode('utf-8')
            encrypted_response = self.encrypt_data(response_msg)
            print(encrypted_response)
            self.mqtt.publish(self.topic, encrypted_response)
            print('der er user')
        else:
            response_msg = 'FLASK:FALSE:TIME'.encode('utf-8')
            encrypted_response = self.encrypt_data(response_msg)
            print(encrypted_response)
            self.mqtt.publish(self.topic, encrypted_response)
            print('der er ikke user')

