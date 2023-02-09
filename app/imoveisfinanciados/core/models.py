# -*- coding: utf-8 -*-

from autoslug import AutoSlugField
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _


class State(models.Model):
    abbr = models.CharField(_("Sigla"), max_length=2)
    name = models.CharField(_("Nome"), max_length=50)

    class Meta:
        # permissions = (
        #     ("view_state", _("Can view State")),
        # )
        verbose_name = _("Estado")
        verbose_name_plural = _("Estados")
        ordering = ["name", "abbr"]

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(_("Nome"), max_length=50)
    state = models.ForeignKey("core.State", on_delete=models.CASCADE, verbose_name=_(
        "Estado"), related_name="cities")
    max_mcmv = models.DecimalField(
        _("Teto: Minha casa minha vida"), max_digits=9, decimal_places=2, blank=True, null=True)
    subsidy_max = models.DecimalField(
        _("Subsídio máximo"), max_digits=9, decimal_places=2, blank=True, null=True)
    subsidy_min = models.DecimalField(
        _("Subsídio mínimo"), max_digits=9, decimal_places=2, blank=True, null=True)
    multsub = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    slug = AutoSlugField(populate_from='name', unique=True)

    # Os dados abaixo são para cálculos considerando dependentes
    d_max_mcmv = models.DecimalField(
        _("Teto: Minha casa minha vida (c/ dependentes)"), max_digits=9, decimal_places=2, blank=True, null=True)
    d_subsidy_max = models.DecimalField(
        _("Subsídio máximo (c/ dependentes)"), max_digits=9, decimal_places=2, blank=True, null=True)
    d_subsidy_min = models.DecimalField(
        _("Subsídio mínimo (c/ dependentes)"), max_digits=9, decimal_places=2, blank=True, null=True)
    d_multsub = models.DecimalField(
        _("multsub (c/ dependentes)"), max_digits=9, decimal_places=2, blank=True, null=True)

    class Meta:
        # permissions = (
        #     ("view_city", _("Can view City")),
        # )
        verbose_name = _("Cidade")
        verbose_name_plural = _("Cidades")
        ordering = ["name", ]

    def __str__(self):
        return str(self.name) if self.name else ''

    def get_absolute_url(self):
        return reverse('city_detail', kwargs={'state': self.state.abbr, 'slug': self.slug})
