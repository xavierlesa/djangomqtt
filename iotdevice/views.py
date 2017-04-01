#!/usr/bin/env python
# -*- coding:utf-8 -*-

import django.dispatch
from django.views.generic import ListView
from .models import DeviceStatus
from .signals import device_publish_signal

class StatusView(ListView):
    queryset = DeviceStatus.objects.filter(channel='ht')
    paginate_by = 12 # 5 horas en intervalos de 5 min.

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by) or self.paginate_by

    def get_context_data(self, **kwargs):
        context = super(StatusView, self).get_context_data(**kwargs)
        context.update({'pid': DeviceStatus.objects.filter(channel='pid').last()})
        
        onoff = self.request.GET.get('onoff')

        if onoff:

            print("publish to 260c4ad9-a5ae-49e6-95ec-b9bc643d1049/onoff => %s" % onoff)
            device_publish_signal.send(sender=self, 
                    device_topic="260c4ad9-a5ae-49e6-95ec-b9bc643d1049/onoff", 
                    message=str(onoff)
                    )

        return context
