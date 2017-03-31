#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import hmac
import uuid

from django.db import models
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from hashlib import sha256
from jsonfield import JSONField
from .signals import device_registration_signal, device_create_signal, device_status_signal

################################################################################
# Workflow for register a device
#
# [DEVICE]  -(sub)-> /ht,/ht/device_id [SERVER]
# [DEVICE]  -(pub)-> [HELO+device_id] --> /ht [SERVER]
# [SERVER]  -(pub)-> [OLEH] --> /ht/device_id



@python_2_unicode_compatible
class Device(models.Model):
    """
    A simple device
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    # Endpoints channles
    channels = models.TextField(help_text="One endpoint by line")
    #set_status = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s <%s>" % (self.name, self.id)

    def get_ht_channel(self):
        return "{}/{}".format(self.id, 'ht')

    def get_channles(self):
        """
        ID + endpoint
        """
        return ["{}/{}".format(self.id, c) for c in  self.channels.splitlines()]


@python_2_unicode_compatible
class DeviceStatus(models.Model):
    """
    Status
    """
    date = models.DateTimeField(auto_now_add=True)
    status = JSONField()
    device = models.ForeignKey(Device)

    class Meta:
        ordering = ['-date']

    def __str__(self, *args, **kwargs):
        return "%s - %s" % (self.date, self.device)

    def get_status(self):
        lines = self.status.splitlines()
        #for i in lines

        return "<br>".join(lines)

@python_2_unicode_compatible
class Register(models.Model):
    """
    Store a key for a device
    """
    key = models.UUIDField(default=uuid.uuid4)
    device = models.ForeignKey(Device)

    def __str__(self):
        return "Register - %s" % self.device

    def save(self, *args, **kwargs):
        super(Register, self).save(*args, **kwargs)
        
        # Propagate signal registration
        device_registration.send(sender=self,  device_id=self.device.id, 
                key=self.key, token=None)
        #self.get_token('')

    def get_token(self, token):
        """
        Create a device token
        """

        token = hmac.new(self.key, self.device.id, sha256).digest().encode("hex").rstrip('\n')
        return token

    #def sign_request(self):
    #    # key = CONSUMER_SECRET& #If you dont have a token yet
    #    key = "%s+%s" % (self.key, self.device.id)


    #    # The Base String as specified here: 
    #    raw = "BASE_STRING" # as specified by oauth

    #    hashed = hmac.new(key, raw, sha256)

    #    # The signature
    #    return hashed.digest().encode("base64").rstrip('\n')

@receiver(device_create_signal)
def get_or_create_device(sender, device_id, name, channels="ht", **kwargs):
    try:
        Device.objects.get(id=device_id)
    except Device.DoesNotExist:
        created = Device.objects.create(id=device_id, name=name, channels=channels)
        print created
    except Exception, E:
        print str(E)
    pass


@receiver(device_status_signal)
def update_status_device(sender, device_id, status, **kwargs):
    DeviceStatus.objects.create(device_id=device_id, status=status)
