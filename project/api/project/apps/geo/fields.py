from django import forms
from core.fields import BaseCustomChoiceField
from apps.geo.models import Country


class CountryChoiceField(BaseCustomChoiceField, forms.ModelChoiceField):
    """
    A field for choosing a single country.
    """

    def provide_queryset(self):
        return Country.objects.all()


class CountryMultipleChoiceField(BaseCustomChoiceField, forms.ModelMultipleChoiceField):
    """
    A field for choosing multiple countries.
    """

    def provide_queryset(self):
        return Country.objects.all()