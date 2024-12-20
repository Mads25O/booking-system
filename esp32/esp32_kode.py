import network
import ssl
from umqtt.simple import MQTTClient
import time
from ucryptolib import aes
import binascii
from mfrc522 import MFRC522
from i2c_lcd import I2cLcd
from machine import Pin
from machine import SoftI2C
from machine import SPI
import time

DEFAULT_I2C_ADDR = 0x27
i2c = SoftI2C(scl=Pin(22, Pin.OUT, Pin.PULL_UP),
              sda=Pin(21, Pin.OUT, Pin.PULL_UP),
              freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 4, 20)

red = Pin(14, Pin.OUT)
grn = Pin(26, Pin.OUT)

spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
spi.init()
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)

# WiFi login information
WIFI_SSID = "Stofa64020"
WIFI_PASSWORD = "ommer99vrede98"

# MQTT Broker information
MQTT_BROKER = "74.234.45.30"
MQTT_PORT = 1883
MQTT_TOPIC = "flask/mqtt/test"
USERNAME = 'esp32'
PASSWORD = '9UGfTxr7sie4'

uid = b'ESP:UID:TIME'
key = b'\xb1\x84\xa6\xe8\x93Jk\xdb\xb5|\xf3{\xa4\x98\x07G#w!\x82\xe8\xb3c\x11$\xeb\x10\x15\xaa?W('
iv = b'\xc1\xd6\n\xd3v\xdae$\xb2\xbd\x17\x8e\xe1\xc4\x1e\xd9'
MODE_CBC = 2

sent_msgs = set()
last_sent_msg = None

def reset_display():
    """Reset LCD display to the initial message."""
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("READY TO SCAN RFID")
    lcd.move_to(0, 1)
    lcd.putstr("Place your card...")


# Opret forbindelse til WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
    print('WiFi connected:', wlan.ifconfig())
    

# --- Kryptering ---
def encrypt_uid(uid_data, key, iv):
    if isinstance(uid_data, str):
        uid_data = str.encode(uid_data)
        print(type(uid_data))
    cipher = aes(key, MODE_CBC, iv)

    pad_len = 16 - (len(uid_data) % 16)
    padded = uid_data + bytes([pad_len] * pad_len)
    
    encrypted = cipher.encrypt(padded)
    return encrypted
    
def decrypt_data(data, key, iv):
    decipher = aes(key, MODE_CBC, iv)
    decrypted = decipher.decrypt(data)
        
    pad_len = decrypted[-1]  # Sidste byte indeholder padding længden
    unpadded_data = decrypted[:-pad_len]
    
    return unpadded_data

# MQTT Callback
def mqtt_callback(topic, data):
    print(f"Received message on topic: {topic.decode('utf-8')} with payload: {data}")
    if data == last_sent_msg:
        print("Duplicate message, ignoring.")
        return
    print(f"Processing new message: {data}")
    decrypted_data = decrypt_data(data, key, iv)
    print(decrypted_data)
    try:
        if isinstance(data, bytes):
            decrypted_data = decrypted_data.decode('utf-8')
        split_decrypted_data = decrypted_data.split(':')
        if split_decrypted_data[1] == 'TRUE':
            print(split_decrypted_data[1])
            grn.value(True)
            red.value(False)
            lcd.move_to(0, 2)
            lcd.putstr("ACCESS GRANTED")
            lcd.move_to(0, 3)
            lcd.putstr(f"Welcome")
            time.sleep(5)  # Tænd grøn LED i 5 sekunder
            grn.value(False)
        if split_decrypted_data[1] == FALSE:
            print('FALSE')
            lcd.move_to(0, 2)
            lcd.putstr("ACCESS DENIED!")
            lcd.move_to(0, 3)
            lcd.putstr("INVALID RFID")
            
            
            # Blink rød LED tre gange
            for _ in range(3):
                red.value(False)
                time.sleep(0.2)
                red.value(True)
                time.sleep(0.2)
        else:
            return None
    except:
        print('FEJL ARRG')

def connect_mqtt():
    client = MQTTClient("ESP32", MQTT_BROKER, port=MQTT_PORT, user=USERNAME, password=PASSWORD)
    client.set_callback(mqtt_callback)
    try:
        client.connect()
        print("MQTT connected to broker")
        client.subscribe(MQTT_TOPIC, qos=1)
        print(f"Subscribed to topic: {MQTT_TOPIC}")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
    return client

# Initialiser rød LED og display
red.value(True)
#reset_display()

# Kør forbindelsen
connect_wifi()

# Opret og forbind til MQTT
mqtt_client = connect_mqtt()


while True:
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            current_time = time.time()
            lcd.clear()
            # Vis RFID UID
            lcd.move_to(0, 0)
            lcd.putstr("RFID Detected!")
            card_id = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
            print(card_id)
            data_to_send = f'ESP:{card_id}:{current_time}'
            encrypted_uid = encrypt_uid(data_to_send, key, iv)
            print("UID:", card_id)
            lcd.move_to(0, 1)
            lcd.putstr(f"UID: {card_id}")
            
            # Reset til standbytilstand

            
            try:
                
                sent_msgs.add(encrypted_uid)
                last_sent_msg = encrypted_uid  # Gem den sidste sendt besked
                mqtt_client.publish(MQTT_TOPIC, encrypted_uid, qos=1)
                print(f'Sent: {encrypted_uid}')
            except KeyboardInterrupt:
                print("Disconnected")
                mqtt_client.disconnect()
                
mqtt_client.wait_msg()
            
        



