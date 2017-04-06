from __future__ import unicode_literals

from django.apps import AppConfig


class IotdeviceConfig(AppConfig):
    name = 'iotdevice'

    def ready(self):
        print "All is ready!"
        
        from django.conf import settings

        if not settings.DEBUG:
            from . import mqtt
            mqtt.client.loop_start()
