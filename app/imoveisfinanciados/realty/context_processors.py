# -*- coding: utf-8 -*-


def user_state(request):
    state = request.session.get('state', 'br')
    return {
        'user_state': state
    }
