from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _

from apps.geo.models import Country


class Command(BaseCommand):
    help = _('Creates and Populates country models')

    def handle(self, *args, **kwargs):
        """
        Create a Django database mirroring the pycountry database.
        """

        print _('Creating country list...')
        Country.pycountry.sync()

