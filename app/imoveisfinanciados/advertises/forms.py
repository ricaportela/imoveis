from django import forms
from imoveisfinanciados.core.models import State, City
from imoveisfinanciados.advertises.models import Banner, ADCity
from django.utils.translation import gettext_lazy as _


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ('title', 'image', 'url')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class ADCityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'state' in self.data:
            state = self.data['state']
            if state:
                qs = State.objects.prefetch_related("cities").all()
                qs = qs.get(pk=state)
                self.fields['cities'].queryset = qs.cities.all()

    title = forms.CharField(
        label=_("Título"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-lg',
                'placeholder': "Como você quer chamar esse anúncio"
            }
        ),
        required=True,
    )

    banner = forms.ModelChoiceField(
        queryset=Banner.objects.all(),
        label=_("Banner"),
        empty_label=_("-- Selecione um banner --"),
        widget=forms.Select(
            attrs={'class': 'form-control input-sm'}),
        required=True,
    )

    active = forms.BooleanField(
        label=_("Ativo?"),
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input'},
        ),
        required=False,
        initial=True,
    )

    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        label=_("Estado"),
        empty_label=_("-- Estado --"),
        widget=forms.Select(
            attrs={'class': 'form-control input-sm dynamic-state'}),
    )

    cities = forms.ModelMultipleChoiceField(
        queryset=City.objects.none(),
        label=_("Município"),
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control input-sm dynamic-city'}),
        required=True
    )

    class Meta:
        model = ADCity
        fields = ('title', 'banner', 'active', 'state', 'cities')
