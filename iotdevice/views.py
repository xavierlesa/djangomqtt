#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.views.generic import ListView
from .models import Device, DeviceStatus
from .mqtt import client, mqtt_topic, mqtt_qos

class StatusView(ListView):
    model = DeviceStatus
    paginate_by = 60 # 5 horas en intervalos de 5 min.

    def get_context_data(self, **kwargs):
        context = super(StatusView, self).get_context_data(**kwargs)
        
        onoff = self.request.GET.get('onoff')

        if onoff:
            #negate = False
            #if onoff.startswith('!'):
            #    negate = True

            #onoff = onoff.replace('!', '')

            #d = {
            #    'a': 1,
            #    'b': 2,
            #    'c': 4
            #}[onoff]

            client.publish("260c4ad9-a5ae-49e6-95ec-b9bc643d1049/onoff", onoff, mqtt_qos)

        return context
