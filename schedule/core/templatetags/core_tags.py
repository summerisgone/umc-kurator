# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.filter
def at(iterable, index):
    return iterable[int(index)]