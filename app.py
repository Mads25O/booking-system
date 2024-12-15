from website import create_app
from flask_mqtt import Mqtt

app = create_app()

# topic = 'test'
# mqtt = Mqtt(app)

# @mqtt.on_connect()
# def handle_connect(client, userdata, flags, rc):
#     print('on_connect client : {} userdata :{} flags :{} rc:{}'.format(client, userdata, flags, rc))
#     mqtt.subscribe("TEST")
#     mqtt.subscribe("death")

# @mqtt.on_subscribe()
# def handle_subscribe(client, userdata, mid, granted_qos):
#     print('on_subscribe client : {} userdata :{} mid :{} granted_qos:{}'.format(client, userdata, mid, granted_qos))


# @mqtt.on_message()
# def handle_message(client, userdata, message):
#     print('on_message client : {} userdata :{} message.topic :{} message.payload :{}'.format(
#     	client, userdata, message.topic, message.payload.decode()))

# @mqtt.on_disconnect()
# def handle_disconnect(client, userdata, rc):
#     print('on_disconnect client : {} userdata :{} rc :{}'.format(client, userdata, rc))
    

# @mqtt.on_log()
# def handle_logging(client, userdata, level, buf):
#     print(level, buf)

# @mqtt_client.on_connect()
# def handle_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print('Connected successfully')
#         mqtt_client.subscribe(topic) # subscribe topic
#     else:
#         print('Bad connection. Code:', rc)

# @mqtt.on_message()
# def handle_mqtt_message(client, userdata, message):
#     data = dict(
#         topic=message.topic,
#         payload=message.payload.decode()
#         )
#     print('Received message on topic: {topic} with payload: {payload}'.format(**data))

if __name__ == '__main__':
    app.run()