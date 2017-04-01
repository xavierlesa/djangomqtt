#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import datetime, time
from uuid import UUID
import paho.mqtt.client as mqtt
from django.conf import settings
from django.dispatch import receiver

from .signals import device_registration_signal, device_create_signal, device_publish_signal, device_status_signal

# mqtt config
MQTT_BROKER_CONFIG = getattr(settings, "MQTT_BROKER_CONFIG", {
    "HOST": "iot.foosible.com",
    "PORT": 1883,
    "USERNAME": "",
    "PASSWORD": "",
    "KEEPALIVE": 120, # 2 minutos
    "QOS": 1,
    "CLIENT_ID": "pyferm",
    "TOPIC": "iferm/ht",
})

# mqtt broker
mqtt_broker_host = MQTT_BROKER_CONFIG.get("HOST")
mqtt_broker_port = MQTT_BROKER_CONFIG.get("PORT")
mqtt_username = MQTT_BROKER_CONFIG.get("USERNAME", "")
mqtt_password = MQTT_BROKER_CONFIG.get("PASSWORD", "")
mqtt_keepalive = MQTT_BROKER_CONFIG.get("KEEPALIVE", 120) # 2 minutos
mqtt_qos = MQTT_BROKER_CONFIG.get("QOS", 1) # QOS True

# mqtt client
mqtt_client_id = MQTT_BROKER_CONFIG.get("CLIENT_ID", "pyferm")

# mqtt pub/sub config
mqtt_topic = MQTT_BROKER_CONFIG.get("TOPIC", "iferm/ht")

# init mqtt
client = mqtt.Client(mqtt_client_id, mqtt_keepalive, mqtt_username, mqtt_password)

registered_channels = [
        (mqtt_topic, mqtt_qos), # canal general
    ]

ht_channels = []


@receiver(device_registration_signal)
def subscribe_to_channels(sender, **kwargs):
    print("subscribe_to_channels signal called with:\r\n%s" % kwargs)

    for channel in sender.device.get_channles():
        if (str(channel), mqtt_qos) not in registered_channels:
            registered_channels.append( (str(channel), mqtt_qos) )

    result = client.subscribe(registered_channels)
    print "suscribed %s" % result


@receiver(device_publish_signal)
def publish_to_device(sender, device_topic, message, **kwargs):
    print("Publish to %s\r\n%s" % (device_topic, message), kwargs)
    from paho.mqtt.publish import single
    single(device_topic, payload=message, qos=mqtt_qos, hostname=mqtt_broker_host,
    port=mqtt_broker_port, client_id=mqtt_client_id, keepalive=mqtt_keepalive)



def on_connect(client, userdata, rc):
    # Subscribe to device channels
    from models import Register

    for device in Register.objects.all():
        for channel in device.device.get_channles():
            registered_channels.append( (str(channel), mqtt_qos) )

    #print "registered_channels", registered_channels

    result = client.subscribe(registered_channels)

def on_message(client, userdata, msg):

    device = msg.topic.split('/')[0]

    if msg.topic == mqtt_topic and not device == 'iferm':
        # Intenta registrar el device si aun no existe.
        print("Intenta registrar el device si aun no existe. \r\n%s" % msg.__dict__)
        try:
            UUID(device, version=4)
        except:
            print("No es un device registrable %s" % device)
        else:
            print("device_create_signal called!!\r\n%s" % device)
            device_create_signal.send(sender=client, device_id=device, name="<Device %s>" % device)

    #elif msg.topic.split('/')[1] == 'ht':
    elif msg.topic.split('/')[1]:
        try:
            data = json.loads(msg.payload)
        except:
            print "topic ht data payload\r\n%s" % msg.payload
        else:
            print("device_status_signal called!!\r\n%s, %s" % (device, data))
            device_status_signal.send(sender=client, device_id=device, status=data, channel=msg.topic.split('/')[1])
            
    else:
        print "data payload\r\n%s" % msg.payload


client.on_connect = on_connect
client.on_message = on_message

# connect
client.connect(mqtt_broker_host, mqtt_broker_port, mqtt_keepalive)
#client.loop_start()
