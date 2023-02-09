# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from six import python_2_unicode_compatible
from django.utils.translation import gettext_lazy as _

@python_2_unicode_compatible
class Simulator(models.Model):
    """ """
    interest = models.DecimalField(
        _("interest"), max_digits=5, decimal_places=4)
    income_max_sub = models.DecimalField(
        _("Renda máxima para o máximo de subsídio"),  # tss
        max_digits=9,
        decimal_places=2
    )
    income_min_sub = models.DecimalField(
        _("Renda máxima para o mínimo de subsídio"),  # zss
        max_digits=9,
        decimal_places=2
    )
    min_income = models.DecimalField(
        _("Renda mínima"),  # n-in
        max_digits=5,
        decimal_places=2
    )

    def __str__(self):
        return "Simulator"


@python_2_unicode_compatible
class Credit(models.Model):
    """ """
    income = models.DecimalField(
        _("Renda"),
        help_text=_(u"Rendas para referência na carta de crédito"),
        max_digits=9,
        decimal_places=2
    )
    value = models.DecimalField(_("Valor"), max_digits=9, decimal_places=2)
    simulator = models.ForeignKey(
        "simulator.Simulator", on_delete=models.CASCADE, related_name="credit")

    class Meta:
        ordering = ['income', 'value']

    def __str__(self):
        return "{0}".format(self.income)


class InstallmentConstant(models.Model):
    TYPES = (
        ('sac', 'SAC'),
        ('price', 'PRICE'),
    )
    type = models.CharField(max_length=5, choices=TYPES)
    value = models.DecimalField(max_digits=3, decimal_places=2)
