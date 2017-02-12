#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from .views import StatusView

urlpatterns = [
    url(r'^$', StatusView.as_view(), name='status'),
]
