# -*- coding: utf-8 -*-


def current_user(request):
    context_vars = {
        'user': request.user,
    }
    return context_vars
