#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django import template

register = template.Library()


@register.assignment_tag
def get_serie(data, index):
    return data[index]
