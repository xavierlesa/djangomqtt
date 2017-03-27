#!/usr/bin/env python
# -*- coding:utf-8 -*-

import django.dispatch
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

            print("publish to 260c4ad9-a5ae-49e6-95ec-b9bc643d1049/onoff => %s" % onoff)
            device_publish.send("260c4ad9-a5ae-49e6-95ec-b9bc643d1049/onoff", str(onoff))

        return context



# Signals for publish to device
device_publish = django.dispatch.Signal(providing_args=["device_topic", "message"])
