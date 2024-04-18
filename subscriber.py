
import paho.mqtt.client as mqtt
import time
from seatable_api import Base, context



def on_connect(mqttc, obj, flags, reason_code, properties):
    print("Connected successfully: " + str(reason_code))


def on_message(mqttc, obj, msg):
    data = {'Topic': str(msg.topic), 'Temperature': str(msg.payload)}
    base.append_row('Data', data)
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
    print("Subscribed: " + str(mid) + " " + str(reason_code_list) + str(properties))


def on_log(mqttc, obj, level, string):
    print(string)


server_url = context.server_url or 'https://cloud.seatable.io'
api_token = context.api_token or '082f58664512a2bb8b9b5bf2e8b5b5e878751bd2'


base = Base(api_token, server_url)
base.auth()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

mqttc.connect("mqtt.eclipseprojects.io", 1883, 60)
subs = base.list_rows('Subscriptions', limit=None)
for i in subs:
    if i['Wildcard'] == "-":
        mqttc.subscribe(f"{i['Name']}")
    else:    
        mqttc.subscribe(f"{i['Name']}/{i['Wildcard']}")
mqttc.loop_forever()