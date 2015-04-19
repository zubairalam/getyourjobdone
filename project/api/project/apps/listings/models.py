from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from embed_video.fields import EmbedVideoField
from imagekit.models import ImageSpecField
from multiselectfield import MultiSelectField
from pilkit.processors import SmartResize

from apps.accounts.models import UserAccount
from apps.accounts.models import User
from apps.core.choices import CalendarChoices, DayChoices
from apps.core.models import ContentModel, NameModel, PublishableModel, Industry, Language, License, Membership, Skill
from apps.geo.models import Location

from .choices import CourseTuitionLevelChoices, CourseTuitionPaymentChoices, CourseTuitionTypeChoices, \
    QualificationChoices, WorkEnvironmentChoices, WorkExperienceChoices, WorkSalaryChoices, WorkTypeChoices
from .helpers import generate_reference_number, generate_salary_range


class ListingModel(ContentModel, PublishableModel):
    """
    Base Listing Model Class.
    """
    reference = models.CharField(unique=True, max_length=15, blank=True, db_index=True,
                                 verbose_name=_('Listing Reference'))
    creator = models.ForeignKey(UserAccount, verbose_name=_('Creator'))
    # creator = models.ForeignKey(User, verbose_name=_('Account Creator'))
    days = MultiSelectField(choices=DayChoices, max_choices=7, blank=True, null=True, verbose_name=_('Days'))
    industry = models.ForeignKey(Industry, verbose_name=_('Industry'))
    location = models.ForeignKey(Location, verbose_name=_('Location'))
    experience = models.PositiveSmallIntegerField(choices=WorkExperienceChoices, verbose_name=_('Experience Required'))
    qualification = models.PositiveSmallIntegerField(choices=QualificationChoices, verbose_name=_('Education Required'))
    languages = models.ManyToManyField(Language, blank=True, null=True, verbose_name=_('Languages'))
    licenses = models.ManyToManyField(License, blank=True, null=True, verbose_name=_('Licenses'))
    memberships = models.ManyToManyField(Membership, blank=True, null=True, verbose_name=_('Memberships'))
    skills = models.ManyToManyField(Skill, blank=True, null=True, verbose_name=_('Skills Required'))
    duration_count = models.PositiveSmallIntegerField(choices=CalendarChoices, verbose_name=_('Duration Count'))
    duration_time = models.IntegerField(verbose_name=_('Duration Time'))
    date_start = models.DateField(verbose_name=_('Start Date'))
    time_start = models.TimeField(verbose_name=_('Start Time'))
    time_end = models.TimeField(verbose_name=_('End Time'))
    image = models.FileField(upload_to='listings', max_length=2048, blank=True, verbose_name=_('Image'))
    thumbnail = ImageSpecField(source='image', processors=[SmartResize(80, 80)], format='png')
    video = EmbedVideoField(blank=True, null=True, verbose_name=_('Video'))


    class Meta:
        abstract = True


class Course(ListingModel):
    """
    Course Concrete Model.
    """
    category = models.PositiveSmallIntegerField(choices=CourseTuitionTypeChoices, verbose_name=_('Category'))
    level = models.PositiveSmallIntegerField(choices=CourseTuitionLevelChoices, verbose_name=_('Course Level'))
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name=_('Price'))
    price_retail = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, blank=True, null=True,
                                       verbose_name=_('Retail Price'))  # useful for businesses.
    price_frequency = models.PositiveSmallIntegerField(choices=CourseTuitionPaymentChoices,
                                                       verbose_name=_('Payment Type'))
    price_negotiable = models.BooleanField(default=False, verbose_name=_('Price Negotiable?'))
    achievement = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('Qualification Achieved'))
    awarded = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('Awarded By'))


    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': str(self.slug)})


@receiver(post_delete, sender=Course)
def course_post_delete_handler(sender, instance, **kwargs):
    try:
        image_storage = instance.image.storage
        image_path = instance.image.path
        image_storage.delete(image_path)
        thumbnail_storage = instance.thumbnail.storage
        thumbnail_path = instance.thumbnail.path
        thumbnail_storage.delete(thumbnail_path)
    except(ValueError, TypeError, IOError, OSError):
        raise Http404


class Tuition(ListingModel):
    """
    Tuition Concrete Model.
    """
    category = models.PositiveSmallIntegerField(choices=CourseTuitionTypeChoices, verbose_name=_('Category'))
    level = models.PositiveSmallIntegerField(choices=CourseTuitionLevelChoices, verbose_name=_('Course Level'))
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name=_('Price'))
    price_frequency = models.PositiveSmallIntegerField(choices=CourseTuitionPaymentChoices,
                                                       default=CourseTuitionPaymentChoices.Month,
                                                       verbose_name=_('Payment Type'))
    price_negotiable = models.BooleanField(default=False, verbose_name=_('Price Negotiable?'))

    class Meta:
        verbose_name = _('Tuition')
        verbose_name_plural = _('Tuitions')

    def get_absolute_url(self):
        return reverse('tuitions:detail', kwargs={'slug': str(self.slug)})


@receiver(post_delete, sender=Tuition)
def tuition_post_delete_handler(sender, instance, **kwargs):
    try:
        image_storage = instance.image.storage
        image_path = instance.image.path
        image_storage.delete(image_path)
        thumbnail_storage = instance.thumbnail.storage
        thumbnail_path = instance.thumbnail.path
        thumbnail_storage.delete(thumbnail_path)
    except(ValueError, TypeError, IOError, OSError):
        raise Http404


class Project(ListingModel):
    """
    Project Concrete Model.
    """
    # need attachment model field to support graphics, docs, etc.??
    # need bid model??
    category = models.PositiveSmallIntegerField(choices=WorkTypeChoices, verbose_name=_('Category'))
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name=_('Budget'))
    price_negotiable = models.BooleanField(default=False, verbose_name=_('Budget Negotiable?'))


    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': str(self.slug)})


class Job(ListingModel):
    """
    Job Concrete Model.
    """
    # related_occupation = models.ForeignKey(Occupation)
    category = models.PositiveSmallIntegerField(choices=CourseTuitionTypeChoices, verbose_name=_('Category'))
    police_record = models.BooleanField(default=True, verbose_name=_('Clean Police Record ?'))
    work_permit = models.BooleanField(default=True, verbose_name=_('Visa Required?'))
    work_environment = models.PositiveSmallIntegerField(choices=WorkEnvironmentChoices,
                                                        verbose_name=_('Work Environment'))
    salary_min = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name=_('Salary Min'))
    salary_max = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name=_('Salary Max'))
    salary_frequency = models.PositiveSmallIntegerField(choices=WorkSalaryChoices,
                                                        verbose_name=_('Payment Type'))
    salary_negotiable = models.BooleanField(default=True, verbose_name=_('Salary Negotiable'))


    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')

    def get_absolute_url(self):
        return reverse('jobs:detail', kwargs={'slug': str(self.slug)})

    def get_location(self):
        if not self.location:
            self.location = self.creator.profile.location
        return self.location

    def get_salary_range(self):
        return generate_salary_range(self.salary_frequency, self.salary_min, self.salary_max)

    def save(self, *args, **kwargs):
        try:
            if not self.id:
                self.reference = generate_reference_number(self.category, self.company)

            # some cleaning up!
            if self.salary_min > self.salary_max:
                self.salary_max = self.salary_min
                self.salary_min = self.salary_max
        except (Exception, ValueError):
            raise Http404
        super(Job, self).save(*args, **kwargs)



class JobBenefit(NameModel):
    job = models.ForeignKey(Job, related_name='job_benefits', verbose_name=_('Job'))

    class Meta:
        verbose_name = _('Benefit')
        verbose_name_plural = _('Benefits')


class JobResponsibility(NameModel):
    job = models.ForeignKey(Job, related_name='job_responsibilities', verbose_name=_('Job'))

    class Meta:
        verbose_name = _('Responsibility')
        verbose_name_plural = _('Responsibilities')
