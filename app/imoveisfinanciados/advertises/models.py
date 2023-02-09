from django.db import models
from django.utils.translation import gettext_lazy as _


class Banner(models.Model):
    title = models.CharField(_('Título'), max_length=100)
    image = models.ImageField(_('Imagem'), upload_to='advertises/')
    url = models.URLField(_('Link destino'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')


class Advertise(models.Model):
    title = models.CharField(_('Título'), max_length=150)
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE, verbose_name=_(
        'Banner'), related_name='%(class)s_advertises')
    active = models.BooleanField(_('Ativo?'), default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class ADNational(Advertise):

    class Meta:
        verbose_name = _('Nacional')
        verbose_name_plural = _('Nacionais')
        get_latest_by = 'created'


class ADState(Advertise):
    states = models.ManyToManyField(
        'core.State', related_name='advertises', verbose_name=_('Estados'))

    class Meta:
        verbose_name = _('Estadual')
        verbose_name_plural = _('Estaduais')
        get_latest_by = 'created'


class ADCity(Advertise):
    cities = models.ManyToManyField(
        'core.City', related_name='advertises', verbose_name=_('Municípios'))

    def related_state(self):
        # import ipdb
        # ipdb.set_trace()
        city = self.cities.all().first()
        if city:
            return city.state.pk
        return

    def cities_list(self):
        return [city.pk for city in self.cities.all()]

    class Meta:
        verbose_name = _('Municipal')
        verbose_name_plural = _('Municipais')
        get_latest_by = 'created'
