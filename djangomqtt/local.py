#!/usr/bin/env python
# -*- coding:utf-8 -*-

from settings import *

MQTT_BROKER_CONFIG = {
    "HOST": "iot.foosible.com",
    "PORT": 1883,
    "USERNAME": "",
    "PASSWORD": "",
    "KEEPALIVE": 120, # 2 minutos
    "QOS": 1,
    "CLIENT_ID": "pyferm-local",
    "TOPIC": "iferm/ht",
}
