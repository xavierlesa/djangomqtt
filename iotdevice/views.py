#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.views.generic import ListView
from .models import Device, DeviceStatus

class StatusView(ListView):
    model = DeviceStatus
    paginate_by = 60 # 5 horas en intervalos de 5 min.

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by) or self.paginate_by

    def get_context_data(self, **kwargs):
        context = super(StatusView, self).get_context_data(**kwargs)
        
        onoff = self.request.GET.get('onoff')

        if onoff:
            from .mqtt import mqtt_client_id, mqtt_keepalive, mqtt_username, mqtt_password, mqtt_qos
            # init mqtt
            client = mqtt.Client(mqtt_client_id, mqtt_keepalive, mqtt_username, mqtt_password)
            #negate = False
            #if onoff.startswith('!'):
            #    negate = True

            #onoff = onoff.replace('!', '')

            #d = {
            #    'a': 1,
            #    'b': 2,
            #    'c': 4
            #}[onoff]

            print("publish to 260c4ad9-a5ae-49e6-95ec-b9bc643d1049/onoff => %s" % onoff)

            print(client.publish("260c4ad9-a5ae-49e6-95ec-b9bc643d1049/onoff", str(onoff), mqtt_qos))

        return context
