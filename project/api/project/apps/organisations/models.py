from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from imagekit.models import ImageSpecField
from pilkit.processors import SmartResize

from apps.core.choices import YearChoices
from apps.core.models import ContentModel, ContactModel, PublishableModel, SocialModel
from apps.geo.models import Location, Country
from apps.core.models import Industry
from apps.accounts.models import UserAccount
from apps.accounts.models import User

from .choices import OrganisationTypes, OrganisationWorkForce


class Organisation(ContentModel, PublishableModel, ContactModel, SocialModel):
    """
    Organisation Concrete Model.
    """
    creator = models.ForeignKey(UserAccount, verbose_name=_('Account Creator'))
    # creator = models.ForeignKey(User, verbose_name=_('Account Creator'))
    category = models.PositiveSmallIntegerField(choices=OrganisationTypes, verbose_name=_('Category'))
    industries = models.ManyToManyField(Industry, related_name='organisation_industries', verbose_name=_('Industries'))
    established = models.PositiveSmallIntegerField(choices=YearChoices, verbose_name=_('Established'))
    country = models.ForeignKey(Country, verbose_name=_('Country'))
    location = models.ForeignKey(Location, verbose_name=_('Location'))
    registration = models.CharField(max_length=75, blank=True, null=True, verbose_name=_('Registration Number'))
    sponsor = models.BooleanField(default=False, verbose_name=_('Offer Work Permit?'))
    training = models.BooleanField(default=False, verbose_name=_('Offer Graduate Training?'))
    workforce = models.PositiveSmallIntegerField(choices=OrganisationWorkForce, verbose_name=_('Workforce'))
    image = models.FileField(upload_to='organisations', max_length=2048, blank=True, verbose_name=_('Logo'))
    thumbnail = ImageSpecField(source='image', processors=[SmartResize(80, 80)], format='png')



    class Meta:
        verbose_name = _('Organisation')
        verbose_name_plural = _('Organisations')

    @staticmethod
    def autocomplete_search_fields():
        return 'id__iexact', 'name__icontains',

    def get_absolute_url(self):
        return reverse('organisations:detail', kwargs={'slug': str(self.slug)})


@receiver(post_delete, sender=Organisation)
def organisation_post_delete_handler(sender, instance, **kwargs):
    try:
        image_storage = instance.image.storage
        image_path = instance.image.path
        image_storage.delete(image_path)
        thumbnail_storage = instance.thumbnail.storage
        thumbnail_path = instance.thumbnail.path
        thumbnail_storage.delete(thumbnail_path)
    except(ValueError, TypeError, IOError, OSError):
        raise Http404


class OrganisationService(models.Model):
    organisation = models.ForeignKey(Organisation, related_name='organisation_services', verbose_name=_('Organisation'))
    service = models.CharField(max_length=128, blank=True, verbose_name=_('Service'))

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')


class OrganisationImage(models.Model):
    organisation = models.ForeignKey(Organisation, related_name='organisation_images', verbose_name=_('Organisation'))
    image = models.FileField(upload_to='organisations', max_length=2048, blank=True, verbose_name=_('Image'))
    thumbnail = ImageSpecField(source='image', processors=[SmartResize(80, 80)], format='png')

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


class OrganisationVideo(models.Model):
    organisation = models.ForeignKey(Organisation, related_name='organisation_videos', verbose_name=_('Organisation'))

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')
