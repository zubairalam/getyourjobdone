from datetime import datetime, timedelta

from django.db import models
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField
from constance import config
from model_utils import Choices
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager

from .helpers import generate_excerpt


class NameModel(models.Model):
    """
    Name abstract base class to provide name and slug.
    """
    name = models.CharField(max_length=128, unique=True, verbose_name=_('Name'))
    slug = AutoSlugField(max_length=128, populate_from='name', unique=True, verbose_name=_('Slug'))

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def __str__(self):
        return self.__unicode__()


class ContentModel(NameModel):
    """
    Content abstract base class to provide name, slug and description.
    """
    description = models.TextField(verbose_name=_('Description'))


    class Meta:
        abstract = True

    def get_excerpt(self):
        return generate_excerpt(self.description, config.SYSTEM_EXCERPT_LENGTH)


class ContactModel(models.Model):
    """
    Contact abstract base class to provide contact.
    """
    email = models.EmailField(blank=True, null=True, verbose_name=_('Email'))
    fax = PhoneNumberField(blank=True, null=True, verbose_name=_('Fax'))
    phone = PhoneNumberField(blank=True, null=True, verbose_name=_('Phone'))
    mobile = PhoneNumberField(blank=True, null=True, verbose_name=_('Mobile'))
    website = models.URLField(blank=True, null=True, verbose_name=_('Website'))

    class Meta:
        abstract = True


class SocialModel(models.Model):
    """
    Social abstract base class to provide Sociable feat.
    """
    facebook = models.URLField(blank=True, null=True, verbose_name=_('Facebook'))
    twitter = models.URLField(blank=True, null=True, verbose_name=_('Twitter'))
    google_plus = models.URLField(blank=True, null=True, verbose_name=_('Google+'))
    linked_in = models.URLField(blank=True, null=True, verbose_name=_('LinkedIn'))
    pinterest = models.URLField(blank=True, null=True, verbose_name=_('Pinterest'))
    youtube = models.URLField(blank=True, null=True, verbose_name=_('Youtube'))


    class Meta:
        abstract = True


class PayableModel(models.Model):
    """
    Payable abstract model to allow concrete classes to inherit payment states
    # modelled after PayPal IPN
    """
    PAYMENT_STATUS = Choices(
        (0, 'Canceled_Reversal', _('Canceled Reversal')),
        (1, 'Completed', _('Completed')),
        (2, 'Created', _('Created')),
        (3, 'Denied', _('Denied')),
        (4, 'Expired', _('Expired')),
        (5, 'Failed', _('Failed')),
        (6, 'Pending', _('Pending')),
        (7, 'Refunded', _('Refunded')),
        (8, 'Reversed', _('Reversed')),
        (9, 'Processed', _('Processed')),
        (10, 'Voided', _('Voided')),
    )

    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name=_('Amount'))
    payment = models.IntegerField(choices=PAYMENT_STATUS, default=PAYMENT_STATUS.Pending,
                                  verbose_name=_('Payment Status'))

    def is_paid(self):
        if self.PAYMENT_STATUS == PayableModel.PAYMENT_STATUS.Completed:
            return True
        return False

    class Meta:
        abstract = True


class CreatedModifiedTimeModel(models.Model):
    """
    Time abstract base class to show created and modified datetimes.
    """
    created = AutoCreatedField(verbose_name=_('Created'))
    modified = AutoLastModifiedField(verbose_name=_('Modified'))

    class Meta:
        abstract = True


class CreatedExpiredModifiedTimeModel(CreatedModifiedTimeModel):
    """
    Time abstract base class to show expired datetimes in conjuction with created & modified.
    """
    # expiry date set 100 years by default ::: needs to be overridden in specific model.
    expired = models.DateTimeField(default=(datetime.utcnow().replace(tzinfo=utc) + timedelta(days=36500)),
                                   verbose_name=_('Expired'))

    class Meta:
        abstract = True


class PublishableModel(CreatedExpiredModifiedTimeModel):
    """
    Publishable abstract base class to give different object statuses.
    """
    PUBLISHED_STATUS = Choices(
        (0, 'Pending', _('Pending')),
        (1, 'Live', _('Live')),
        (2, 'Flagged', _('Flagged')),
        (3, 'Archived', _('Archived')),

    )
    published = models.IntegerField(choices=PUBLISHED_STATUS, default=PUBLISHED_STATUS.Pending,
                                    verbose_name=_('Published Status'))

    @staticmethod
    def is_live(self):
        if self.PUBLISHED_STATUS == PublishableModel.PUBLISHED_STATUS.Live:
            return True
        return False

    class Meta:
        abstract = True


class TaggableModel(models.Model):
    """
    Taggable abstract base class to allow tags support.
    """
    tags = TaggableManager(blank=True, verbose_name=_('Tags'))

    class Meta:
        abstract = True


class Industry(ContentModel):
    """
    Industry Concrete Model.
    """
    parent = models.ForeignKey('self', blank=True, null=True, related_name='parent_industries')

    class Meta:
        verbose_name = _('Industry')
        verbose_name_plural = _('Industries')

    @staticmethod
    def autocomplete_search_fields():
        return 'id__iexact', 'name__icontains',



class Language(ContentModel):
    """
    Language Concrete Model.
    """

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')


class License(ContentModel):
    """
    License Concrete Model.
    """

    class Meta:
        verbose_name = _('License')
        verbose_name_plural = _('Licenses')


class Membership(ContentModel):
    """
    Membership Concrete Model.
    """

    class Meta:
        verbose_name = _('Membership')
        verbose_name_plural = _('Memberships')


class Skill(ContentModel):
    """
    Skill Concrete Model.
    """

    class Meta:
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')


class Qualification(ContentModel):
    """
    Qualification Concrete Model.
    """

    class Meta:
        verbose_name = _('Qualification')
        verbose_name_plural = _('Qualifications')


class WorkExperience(ContentModel):
    """
    Work Experience Concrete Model.
    """

    class Meta:
        verbose_name = _('Work Experience')
        verbose_name_plural = _('Work Experiences')