#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import datetime, time
import paho.mqtt.client as mqtt

from models import Device, DeviceStatus, Register


# mqtt server
mqtt_broker_host = "iot.foosible.com"
mqtt_broker_port = 1883
mqtt_username = ""
mqtt_password = ""
mqtt_keepalive = 120 # 2 minutos
mqtt_qos = 1

# mqtt client
mqtt_client_id = "pyferm"


# mqtt pub/sub config
mqtt_topic = "iferm/ht"

# init mqtt
client = mqtt.Client(mqtt_client_id, mqtt_keepalive, mqtt_username, mqtt_password)

registered_channels = [
        (mqtt_topic, mqtt_qos), # canal general
    ]

ht_channels = []

def on_connect(client, userdata, rc):
    # Subscribe to device channels

    for device in Register.objects.all():
        for channel in device.device.get_channles():
            registered_channels.append( (str(channel), mqtt_qos) )

    print "registered_channels", registered_channels

    result = client.subscribe(registered_channels)

def on_message(client, userdata, msg):
    print msg.topic
    if msg.topic.split('/')[1] == 'ht':
        try:
            data = json.loads(msg.payload)
        except:
            print msg.payload
        else:
            device = msg.topic.split('/')[0]
            status = DeviceStatus.objects.create(device_id=device, status=data)
            print data
            
    else:
        print msg.payload



client.on_connect = on_connect
client.on_message = on_message

# connect
client.connect(mqtt_broker_host, mqtt_broker_port, mqtt_keepalive)
