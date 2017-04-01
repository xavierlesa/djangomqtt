#!/usr/bin/env python
# -*- coding:utf-8 -*-

import django.dispatch

# Signals for auto registration
device_registration_signal = django.dispatch.Signal(providing_args=["device_id", "key", "token"])

# Signals for create
device_create_signal = django.dispatch.Signal(providing_args=["device_id", "name", "channles"])

# Signals status
device_status_signal = django.dispatch.Signal(providing_args=["device_id", "status", "channel"])

# Signals for publish to device
device_publish_signal = django.dispatch.Signal(providing_args=["device_topic", "message"])
