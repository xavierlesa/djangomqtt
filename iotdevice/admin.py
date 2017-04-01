#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.contrib import admin
from django.utils.safestring import mark_safe
from models import Device, DeviceStatus, Register


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'get_ht_channel']


class DeviceStatusAdmin(admin.ModelAdmin):
    list_display = ['date', 'device', 'status', 'channel']
    list_filter = ['channel']
    date_hierarchy = 'date'
    

admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceStatus, DeviceStatusAdmin)
admin.site.register(Register)
