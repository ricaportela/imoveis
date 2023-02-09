# -*- coding: utf-8 -*-

from django import template
from ..money import money_format as mformat


register = template.Library()


@register.filter(name='money_format')
def money_format(value):
    return mformat(value)
