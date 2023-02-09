# -*- coding: utf-8 -*-


class StateListMixin(object):

    def get_state(self):
        return self.request.session.get('state', "")

    def set_state(self, state):
        self.request.session["state"] = state
        self.request.session.set_expiry(0)

    def get_context_data(self, **kwargs):
        kwargs = super(StateListMixin, self).get_context_data(**kwargs)
        state_ = self.request.GET.get("state")
        if state_:
            self.set_state(self.request.GET.get("state"))
        kwargs["state"] = self.get_state()
        return kwargs