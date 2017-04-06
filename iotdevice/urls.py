#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from .views import StatusView, PIDAutoView

urlpatterns = [
    url(r'^$', StatusView.as_view(), name='status'),
    url(r'^(?P<pk>[a-z0-9\-]+)/?$', PIDAutoView.as_view(), name='pid_auto'),
]
