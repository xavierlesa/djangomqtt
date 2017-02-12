#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import hmac
import uuid

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from hashlib import sha256

from jsonfield import JSONField

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
