from django import forms
from django.contrib import admin
from apps.geo.models import Country, Location, Nationality
from apps.geo.widgets import LocationWithMapWidget


class CountryAdmin(admin.ModelAdmin):
    """
    Country Admin Class.
    """
    fields = ('name', 'formal_name', 'alpha2', 'alpha3', 'numeric', )
    list_display = ('name', 'formal_name', 'slug',)
    list_per_page = 50
    search_fields = ('name', 'formal_name',)
    ordering = ('name',)


admin.site.register(Country, CountryAdmin)


class LocationAdmin(admin.ModelAdmin):
    """
    Location Admin Class.
    """
    fields = ('address', 'computed_address', 'latitude', 'longitude', 'geocode_error',)
    list_display = ('address', 'computed_address', 'latitude', 'longitude', 'geocode_error',)
    list_per_page = 100
    list_filter = ('geocode_error',)
    search_fields = ('address', 'computed_address')
    ordering = ('address',)

    class form(forms.ModelForm):
        class Meta:
            widgets = {
                'address': LocationWithMapWidget({'class': 'vTextField'})
            }


admin.site.register(Location, LocationAdmin)


class NationalityAdmin(admin.ModelAdmin):
    """
    Nationality Admin Class.
    """

    fields = ('name', 'country',)
    list_display = ('name', 'country', 'slug',)
    list_per_page = 50
    search_fields = ('name', 'country',)
    ordering = ('name',)


admin.site.register(Nationality, NationalityAdmin)