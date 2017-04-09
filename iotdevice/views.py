#!/usr/bin/env python
# -*- coding:utf-8 -*-

import django.dispatch
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .models import DeviceStatus, Device
from .signals import device_publish_signal


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context


class PIDAutoView(JSONResponseMixin, DetailView):
    model = Device

    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format') == 'json':
            data = {'pid': DeviceStatus.objects.filter(channel='pid').first().status} #first porque esta como -date
            return self.render_to_json_response(data)
        else:
            return super(PIDAutoView, self).render_to_response(context)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(PIDAutoView, self).dispatch(*args, **kwargs)


class StatusView(ListView):
    queryset = DeviceStatus.objects.filter(channel='ht')
    paginate_by = 12 # 5 horas en intervalos de 5 min.

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by) or self.paginate_by

    def get_context_data(self, **kwargs):
        context = super(StatusView, self).get_context_data(**kwargs)
        context.update({'pid': DeviceStatus.objects.filter(channel='pid').first()}) #first porque esta como -date
        
        onoff = self.request.GET.get('onoff')

        if onoff:

            print("publish to 260c4ad9-a5ae-49e6-95ec-b9bc643d1049/onoff => %s" % onoff)
            device_publish_signal.send(sender=self, 
                    device_topic="260c4ad9-a5ae-49e6-95ec-b9bc643d1049/onoff", 
                    message=str(onoff)
                    )

        return context
