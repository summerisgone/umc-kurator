# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.filter
def attrs(field, attribute_description):
    attributes = attribute_description.split(",")
    for attribute in attributes:
        attr_name, attr_value = attribute.split('=')
        attr_value = attr_value.strip('"').strip("'")
        field.field.widget.attrs[attr_name] = attr_value
    return field