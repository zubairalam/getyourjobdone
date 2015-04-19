from django.conf import settings

from django.db import models

from apps.accounts.models import AbstractProfile

from django.utils.translation import ugettext as _
from django.core.validators import URLValidator


class FacebookUserLocation(models.Model):
    location_id = models.TextField(verbose_name=_('Location Id'))
    location_name = models.TextField(verbose_name=_('Location Name'))


class FacebookFriends(models.Model):
    pass


class FacebookWorkHistory(models.Model):
    employer_id = models.TextField(verbose_name=_('Employer Id'))
    employer_name = models.TextField(verbose_name=_('Employer Name'))
    location_id = models.TextField(verbose_name=_('Location Id'))
    location_name = models.TextField(verbose_name=_('Location Name'))
    position_id = models.TextField(verbose_name=_('Position Id'))
    position_name = models.TextField(verbose_name=_('Position Name'))
    start_date = models.TextField(verbose_name=_('Start Date'))


class FacebookEducationHistory(models.Model):
    degree_id = models.TextField(verbose_name=_('Degree Id'))
    degree_name = models.TextField(verbose_name=_('Degree Name'))
    institute_type = models.TextField(verbose_name=_('Institute Type'))
    school_id = models.TextField(verbose_name=_('School Id'))
    school_name = models.TextField(verbose_name=_('School Name'))
    year_id = models.TextField(verbose_name=_('Year Id'))
    year_name = models.TextField(verbose_name=_('Year Name'))


class FacebookActivities(models.Model):
    pass


class FacebookGroups(models.Model):
    pass


class FacebookEvents(models.Model):
    pass

# facebook profile data.
#
class FacebookProfile(AbstractProfile):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='facebook_profile', verbose_name=_('User'))
    profile_id = models.TextField(verbose_name=_('User Id'))
    profile_pic = models.TextField(validators=[URLValidator()], verbose_name=_('Profile Photo'))
    website = models.TextField(validators=[URLValidator()], verbose_name=_('Website'))
    # friends = model.ManyToManyField(FacebookFriends, verbose_name=_('Friends'))
    location = models.ForeignKey(FacebookUserLocation, blank=True, null=True, verbose_name=_('Location'))
    work_history = models.ManyToManyField(FacebookWorkHistory, blank=True, null=True, verbose_name=_('Work History'))
    education_history = models.ManyToManyField(FacebookEducationHistory, blank=True, null=True, verbose_name='Education History')
    # activities = models.ManyToManyField(FacebookActivities, verbose_name=_('Activities'))
    # groups = models.ManyToManyField(FacebookGroups, verbose_name=_('Groups'))
    # events = models.ManyToManyField(FacebookEvents, verbose_name=_('Events'))

class LinkedInEducationHistory(models.Model):
    degree_id= models.TextField(verbose_name=_('Degree Id'))
    degree = models.TextField(verbose_name=_('Degree'))
    activities = models.TextField(verbose_name=_('Activities'))
    field_of_study = models.TextField(verbose_name=_('Field of Study'))
    notes = models.TextField(verbose_name=_('Notes'))
    school_name = models.TextField(verbose_name=_('School Name'))
    start_date_year = models.TextField(verbose_name=_('Start Date'))
    end_date_year = models.TextField(verbose_name=_('End Date'))

class LinkedInWorkHistory(models.Model):
    company_id = models.TextField(verbose_name=_('Company Id'))
    company = models.TextField(verbose_name=_('Company'))
    is_current = models.TextField(verbose_name=_('Is Current'))
    summary = models.TextField(verbose_name=_('Summary'))
    title = models.TextField(verbose_name=_('Title'))
    start_date_month = models.TextField(verbose_name=_('Start Month'))
    start_date_year = models.TextField(verbose_name=_('Start Year'))
    end_date_month = models.TextField(verbose_name=_('End Month'))
    end_date_year = models.TextField(verbose_name=_('End Year'))

class LinkedInSkills(models.Model):
    skill_id = models.TextField(verbose_name=_('Skill Id'))
    skill = models.TextField(verbose_name=_('Skill'))

class LinkedInFriends(models.Model):
    pass

class LinkedInProfile(AbstractProfile):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='linkedin_profile', verbose_name=_('User'))
    profile_id = models.TextField(verbose_name=_('User Id'))
    profile_pic = models.TextField(validators=[URLValidator()], verbose_name=_('Profile Photo'))
    website = models.TextField(validators=[URLValidator()], verbose_name=_('Website'))
    location = models.TextField(verbose_name=_('Location'))
    #friends = models.ManyToManyField(LinkedInFriends, verbose_name=_('Friends'))
    #location = models.ForeignKey(FacebookUserLocation, blank=True, null=True, verbose_name=_('Location'))
    work_history = models.ManyToManyField(LinkedInWorkHistory, blank=True, null=True, verbose_name=_('Work History'))
    education_history = models.ManyToManyField(LinkedInEducationHistory, blank=True, null=True, verbose_name='Education History')
    skills = models.ManyToManyField(LinkedInSkills, blank=True, null=True, verbose_name=_('Skills'))
    # activities = models.ManyToManyField(FacebookActivities, verbose_name=_('Activities'))
    # groups = models.ManyToManyField(FacebookGroups, verbose_name=_('Groups'))
    # events = models.ManyToManyField(FacebookEvents, verbose_name=_('Events'))
