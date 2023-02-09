import re
from django import template
from imoveisfinanciados.advertises.models import ADNational
from imoveisfinanciados.core.models import State, City


register = template.Library()


@register.simple_tag()
def ad_national():
    ad = ADNational.objects.filter(active=True)
    if ad.count() > 0:
        return ad.latest()
    return {}


def _get_current_state(path):
    state_re = re.compile(r'^\/([a-z]{2})\/')
    state = state_re.findall(path)
    if len(state) > 0:
        return state[0].upper()
    return ''


@register.simple_tag(takes_context=True)
def ad_state(context):
    state = State.objects.filter(abbr=_get_current_state(
        context.request.get_full_path())).first()
    if state:
        ad = state.advertises.filter(active=True)
        if ad.count() > 0:
            return ad.latest()
    return {}


def _get_current_city(path):
    city_re = re.compile(r'^\/[a-z]{2}\/([-a-z]+)\/')
    city = city_re.findall(path)
    if len(city) > 0:
        return city[0]
    return ''


@register.simple_tag(takes_context=True)
def ad_city(context):
    city = City.objects.filter(slug=_get_current_city(
        context.request.get_full_path())).first()
    if city:
        ad = city.advertises.filter(active=True)
        if ad.count() > 0:
            return ad.latest()
    return {}
