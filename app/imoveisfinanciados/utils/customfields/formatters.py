from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaultfilters import floatformat


def decimal_to_real(value, precision=2):
    '''
    Receives a Decimal instance and returns a string formatted as brazilian Real currency:
    12,234.00. Without the "R$".
    '''
    value = floatformat(value, precision)
    value, decimal = value.split('.')
    value = intcomma(value)
    value = value.replace(',', '.') + ',' + decimal
    return value
