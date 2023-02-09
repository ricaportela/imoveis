# -*- coding: utf-8 -*-

from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from imoveisfinanciados.core.models import State, City
from imoveisfinanciados.utils.slug import unique_slugify


def realty_slugify(title, type, size, city, state):
    return "{0} {1} {2}m2 {3} {4}".format(title, type, size, city, state)


class Realty(models.Model):
    """ """
    TYPES = (
        ("apt", _("Apartamento")),
        ("casa", _("Casa")),
        ("cond", _("Condomínio"))
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name=_("Usuário"))
    title = models.CharField(_("Título do anúncio"), max_length=150)
    description = models.TextField(_("Descrição"), blank=True, null=True)
    type = models.CharField(_("Tipo do imóvel"), max_length=4, choices=TYPES)
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, verbose_name=_("Estado"))
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name=_("Cidade"))
    value = models.DecimalField(_("Preço"), max_digits=11, decimal_places=2)
    bedroom = models.IntegerField(_("Quartos"))
    bathroom = models.IntegerField(_("Banheiros"))
    size = models.IntegerField(_("Metros quadrados"))
    main_image = models.ImageField(_("Foto principal"), upload_to="realties/")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = 'realty'
        verbose_name = _("Imóvel")
        verbose_name_plural = _("Imóveis")
        ordering = ['-created', '-modified', 'value']

    def __str__(self):
        return str(self.title) if self.title else ''

    def __repr__(self):
        return '<Realty {}>'.format(self.title)

    def save(self, **kwargs):
        slug = realty_slugify(
            self.title, self.type, self.size, self.city, self.state
        )
        unique_slugify(self, slug)
        super(Realty, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse('realty:view', kwargs={'slug': self.slug})

    def cover(self):
        return self.main_image

    def local_ad(self):
        ad = self.city.advertises.filter(active=True)
        if ad:
            return ad.latest()


class Photo(models.Model):
    """ """
    title = models.CharField(_("Título"), max_length=50, blank=True, null=True)
    image = models.ImageField(_("Foto"), upload_to="realties/")
    realty = models.ForeignKey(
        Realty, on_delete=models.CASCADE, verbose_name="Imóvel", related_name='photos')

    class Meta:
        verbose_name = _("Foto")
        verbose_name_plural = _("Fotos")

    def __str__(self):
        return str(self.title) if self.title else ''
