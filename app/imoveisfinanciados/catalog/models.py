# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.urls import reverse
from django.db import models
from six import python_2_unicode_compatible
from django.utils.translation import gettext_lazy as _
from imoveisfinanciados.utils.slug import unique_slugify


class CatalogQuerySet(models.QuerySet):

    def imobiliarias(self):
        return self.filter(is_active=True).filter(type__type__exact='imobiliaria')

    def correspondentes(self):
        return self.filter(is_active=True).filter(type__type__exact='correspondente')

    def incorporadoras(self):
        return self.filter(is_active=True).filter(type__type__exact='incorporadora')


class CatalogManager(models.Manager):

    def get_queryset(self):
        return CatalogQuerySet(self.model, using=self._db)

    def imobiliarias(self):
        return self.get_queryset().imobiliarias()

    def correspondentes(self):
        return self.get_queryset().correspondentes()

    def incorporadoras(self):
        return self.get_queryset().incorporadoras()


@python_2_unicode_compatible
class CatalogType(models.Model):
    """
    """
    TYPE = (
        ("imobiliaria", _("Imobiliária")),
        ("correspondente", _("Correspondente Bancário")),
        ("incorporadora", _("Incorporadora")),
    )
    type = models.CharField(_("Tipo"), max_length=25, choices=TYPE)
    price = models.DecimalField("Preço", max_digits=7, decimal_places=2)

    class Meta:
        db_table = "catalog_type"
        verbose_name = _("Tipo de catálogo")
        verbose_name_plural = _("Tipos de catálogos")

    def __str__(self):
        return self.type


@python_2_unicode_compatible
class Catalog(models.Model):
    """
    """
    type = models.ForeignKey("catalog.CatalogType", on_delete=models.CASCADE,
                             verbose_name=_("Tipo"), related_name="catalogs")
    name = models.CharField(_("Nome"), max_length=150)
    localization = models.CharField(
        _("Localização"), max_length=150, blank=True)
    email = models.EmailField(_("Email do catálogo"))
    is_active = models.BooleanField(_("Ativo?"), default=False)
    state = models.ForeignKey("core.State", on_delete=models.CASCADE, verbose_name=_(
        "Estado"), related_name="catalogs")
    city = models.ForeignKey("core.City", on_delete=models.CASCADE, verbose_name=_(
        "Cidade"), related_name="catalogs")
    logo = models.ImageField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_(
        "Usuário"), related_name="catalogs")
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = CatalogManager()

    class Meta:
        db_table = "catalog"
        verbose_name = _("Catálogo")
        verbose_name_plural = _("Catálogos")

    def __str__(self):
        return "[{0}] {1}".format(self.type, self.name)

    def save(self, **kwargs):
        slug = self._catalog_slugify(self.type.get_type_display(), self.name)
        unique_slugify(self, slug)
        super(Catalog, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse('catalog:view', kwargs={'slug': self.slug})

    def _catalog_slugify(self, type, name):
        return "{0} {1}".format(type, name)


@python_2_unicode_compatible
class CatalogPhone(models.Model):

    TYPES = (
        ("geral", _("Geral")),
        ("aluguel", _("Aluguel")),
        ("venda", _("Venda"))
    )
    type = models.CharField(_("Tipo"), max_length=7,
                            choices=TYPES, default="geral")
    number = models.CharField(_("Número"), max_length=15)
    catalog = models.ForeignKey(
        "catalog.Catalog", on_delete=models.CASCADE, related_name="phones", verbose_name=_("Catálogo"))

    class Meta:
        db_table = "catalog_phone"
        verbose_name = _("Número do catálogo")
        verbose_name_plural = _("Números do catálogo")

    def __str__(self):
        return self.number


@python_2_unicode_compatible
class PaymentHistory(models.Model):
    """ """
    STATUS = (
        ("1", "Aguardando pagamento"),
        ("2", "Em análise"),
        ("3", "Paga"),
        ("4", "Disponível"),
        ("5", "Em disputa"),
        ("6", "Devolvida"),
        ("7", "Cancelada"),
    )

    status = models.CharField(max_length=1, choices=STATUS, default="1")
    transaction = models.CharField(max_length=100, blank=True)
    modified = models.DateTimeField(auto_now=True)
    catalog = models.ForeignKey("catalog.Catalog", on_delete=models.CASCADE, verbose_name=_(
        "Catálogo"), related_name="payments")

    class Meta:
        db_table = "payment_history"
        verbose_name = _("Histórico de pagamento")
        verbose_name_plural = _("Histórico de pagamentos")

    def __str__(self):
        return self.get_status_display()
