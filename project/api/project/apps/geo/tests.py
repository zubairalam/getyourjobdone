from django.test import TestCase
from apps.geo.models import Country


class CountryTest(TestCase):
    """
    Tests for the Country model.
    """

    # def test_sync(self):
    #     """
    #     The Country instances should exactly match the pycountry countries.
    #     """
    #
    #     Country.countries.sync()
    #     for country in pycountry.countries:
    #         country = Country.objects.get(alpha2=country.alpha2)
    #         for attr in ['alpha2', 'alpha3', 'numeric', 'title', 'formal_name']:
    #             if hasattr(country, attr):
    #                 self.assertEqual(getattr(country, attr), getattr(country, attr))

