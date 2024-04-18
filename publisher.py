
import paho.mqtt.client as mqtt
import random
import time

def on_connect(mqttc, obj, flags, reason_code, properties):
    print("reason_code: " + str(reason_code))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid, reason_code, properties):
    print("mid: " + str(mid))


def on_log(mqttc, obj, level, string):
    print(string)



mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
#mqttc.on_log = on_log
mqttc.connect("mqtt.eclipseprojects.io", 1883, 60)

mqttc.loop_start()

while True:
    temp= 20+random.random()*10
    time.sleep(5)
    (rc, mid) = mqttc.publish("temp/iot1", temp, qos=2)        
