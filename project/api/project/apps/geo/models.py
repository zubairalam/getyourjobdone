import logging
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.core.models import NameModel
from apps.geo import geocode
from apps.geo.managers import CountryManager, CustomCountryManager

logger = logging.getLogger(__name__)


class Country(NameModel):
    """
    Country Concrete Model covered by the ISO 3166-1 standard.
    """
    formal_name = models.CharField(max_length=75, null=True, blank=True, verbose_name=_('Official Name'))
    alpha2 = models.CharField(max_length=2, unique=True, verbose_name=_('Alpha-2 Code'), )
    alpha3 = models.CharField(max_length=3, unique=True, verbose_name=_('Alpha-3 Code'))
    numeric = models.CharField(max_length=3, verbose_name=_('Numeric Code'))
    objects = CountryManager()
    countries = CustomCountryManager()

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    def natural_key(self):
        return self.alpha3


class Location(models.Model):
    address = models.CharField(max_length=255, unique=True, verbose_name=_('Address'))
    computed_address = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Computed Address'))
    latitude = models.FloatField(null=True, blank=True, verbose_name=_('Latitude'))
    longitude = models.FloatField(null=True, blank=True, verbose_name=_('Longitude'))
    geocode_error = models.BooleanField(default=False, verbose_name=_('Geocode Error'))

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    @staticmethod
    def autocomplete_search_fields():
        return 'id__iexact', 'address__icontains',


    def fill_geocode_data(self):
        if not self.address:
            self.geocode_error = True
            return
        try:
            do_geocode = getattr(settings, 'MAPS_GEOCODE', geocode.google_v3)
            self.computed_address, (self.latitude, self.longitude,) = do_geocode(self.address)
            self.geocode_error = False
        except geocode.Error as e:
            try:
                logger.error(e)
            except Exception:
                logger.error('Geocoding error for location %s', self.address)
            self.geocode_error = True
            # TODO: store the exception

    def save(self, *args, **kwargs):
        # fill geocode data if it is unknown
        if (self.longitude is None) or (self.latitude is None):
            self.fill_geocode_data()
        super(Location, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{0}'.format(self.address)

    def __str__(self):
        return self.__unicode__()


class Nationality(NameModel):
    """
    Nationality Concrete Model.
    """
    country = models.ForeignKey(Country, verbose_name=_('Country'))

    class Meta:
        verbose_name = _('Nationality')
        verbose_name_plural = _('Nationalities')
