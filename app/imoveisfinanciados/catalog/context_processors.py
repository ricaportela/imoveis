# -*- coding: utf-8 -*-

from .models import Catalog


def has_catalog(request):
    user = request.user

    if isinstance(user.pk, int):
        uc = Catalog.objects.filter(user__exact=request.user)
    else:
        uc = False
    context_vars = {
        'has_catalog': uc and True or False,
    }
    return context_vars
