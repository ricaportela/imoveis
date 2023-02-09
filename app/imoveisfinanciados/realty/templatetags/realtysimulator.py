# -*- coding: utf-8 -*-

from django import template

from imoveisfinanciados.utils.money import money_format


register = template.Library()

@register.simple_tag
def down_payment(realty_value, fundable):
    result = realty_value - fundable
    if result < 0:
        result = 0
    return money_format(result)