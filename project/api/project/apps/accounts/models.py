import hashlib

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import URLValidator

from imagekit.models import ImageSpecField
from pilkit.processors import SmartResize

from apps.core.models import ContactModel, CreatedModifiedTimeModel, PublishableModel, SocialModel

from .choices import UserAccountTypeChoices, UserGenderChoices, UserRelationshipChoices, UserReferralChoices, \
    UserTitleChoices, LoginChoices
from .managers import CustomUserManager


class AbstractCustomUser(AbstractBaseUser, PermissionsMixin, CreatedModifiedTimeModel):
    """
    Custom User with the same behaviour as Django's default User but
    without a username field. Uses email as the USERNAME_FIELD for
    authentication.
    Inherits from both the AbstractBaseUser and PermissionMixin.
    The following attributes are inherited from the superclasses:
        * password
        * last_login
        * is_superuser
    """

    class Meta:
        abstract = True


class User(AbstractCustomUser):
    """
    Concrete class of AbstractCustomUser.
    """
    email = models.EmailField(unique=True, db_index=True, verbose_name=_('Primary Email'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Staff Status'))
    hash = models.CharField(max_length=36, blank=True, null=True, verbose_name=_('Verification Hash'))
    # first_name = models.CharField(max_length=100, verbose_name=_('First Name(s)'))
    # last_name = models.CharField(max_length=100, verbose_name=_('Last Name'))
    active = models.BooleanField(default=False, verbose_name=_('Active?'))
    terms = models.BooleanField(default=True, verbose_name=_('Accept T&Cs?'))

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ('first_name', 'last_name',)

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')

    @staticmethod
    def autocomplete_search_fields():
        return 'id__iexact', 'email__icontains',


    def get_email(self):
        """
        Returns the Registration Email of the User.
        """
        return '{0}'.format(self.email)

    def get_short_name(self):
        """
        Returns the First Name of the User.
        """
        profile = self.get_profile()
        return '{0}'.format(profile.first_name)

    def get_full_name(self):
        """
        Returns the First + Last Names of the User.
        """
        profile = self.get_profile()
        return '{0} {1}'.format(profile.first_name, profile.last_name)

    #def get_account(self):
    #    """
    #    Returns the UserAccount Model for the User.
    #    """
    #    return UserAccount.objects.get(user=self)

    def get_setting(self):
        """
        Returns the UserSetting Model for the User.
        """
        return UserSetting.objects.get(user=self)


    def get_profile(self):
        """
        Returns the UserProfile Model for the User.
        """
        return UserProfile.objects.get(user=self)

    # def get_full_name_with_salutation(self):
    #     """
    #     Returns the Designation of the User.
    #     """
    #     try:
    #         profile = self.get_profile()
    #         if profile:
    #             designation = UserTitleChoices[profile.designation][1]
    #             if designation:
    #                 return u'{0} {1} {2}'.format(designation, self.first_name, self.last_name)
    #     except(Exception, ValueError, TypeError):
    #         return self.get_full_name()


    def get_picture(self):
        """
        Returns the Profile Picture of the User.
        In case no picture is uploaded, gravatar lookup on the primary_email occurs.
        """
        try:
            if self.get_profile():
                if self.get_profile().image:
                    return self.get_profile().image.url
                    #return self.get_profile().image.name
            return '{0}'.format(settings.USER_AVATAR)
        except(Exception, ValueError, IOError, TypeError):
            md5_hexed_email = hashlib.md5(self.email.encode('utf-8')).hexdigest()
            return 'https://secure.gravatar.com/avatar/{0}?default=identicon'.format(md5_hexed_email)

    def get_social_accounts(self):
        """
        Returns a dictionary of social accounts attached to a user account
        """
        social_accounts = {}
        try:
            social_accounts['linkedin'] = LinkedInProfile.objects.get(user=self)
        except:
            pass
        try:
            social_accounts['facebook'] = FacebookProfile.objects.get(user=self)
        except:
            pass

        return social_accounts


    # def email_user(self, subject, message, from_email=None):
    # '''
    # Sends an Email to the User.
    # '''
    # send_mail(subject, message, from_email, [self.email])


    # def __unicode__(self):
    #     return u'{0}'.format(self.get_full_name())


    # def __str__(self):
    #     return self.__unicode__()


class UserAccount(PublishableModel):
   """
   Account Concrete Model.
   """
   user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_account', verbose_name=_('User'))
   account = models.PositiveSmallIntegerField(choices=UserAccountTypeChoices, verbose_name=_('Account Type'))

   @staticmethod
   def autocomplete_search_fields():
       return 'id__iexact', 'user__email__icontains', 'user__first_name__icontains', 'user__last_name__icontains',

   class Meta:
       verbose_name = _('User Account')
       verbose_name_plural = _('Account Info')

   def __unicode__(self):
       return u'{0}'.format(self.user)

   def __str__(self):
       return self.__unicode__()


class AbstractProfile(models.Model):
    # email = models.EmailField(unique=True, db_index=True, verbose_name=_('Primary Email'))
    first_name = models.CharField(max_length=100, verbose_name=_('First Name(s)'))
    last_name = models.CharField(max_length=100, verbose_name=_('Last Name'))
    biography = models.TextField(blank=True, null=True, verbose_name=_('Biography'))
    #birthday = models.DateField(blank=True, null=True, verbose_name=_('Date of Birth'))
    birthday = models.TextField(blank=True, null=True, verbose_name=_('Date of Birth'))
    designation = models.PositiveSmallIntegerField(choices=UserTitleChoices, blank=True, null=True,
                                                   verbose_name=_('Designation'))
    gender = models.PositiveSmallIntegerField(choices=UserGenderChoices, blank=True, null=True,
                                              verbose_name=_('Gender'))
    avatar = models.FileField(upload_to='users', max_length=2048, blank=True, verbose_name=_('Avatar'))
    image = models.FileField(upload_to='users', max_length=2048, blank=True, verbose_name=_('Picture'))
    thumbnail = ImageSpecField(source='image', processors=[SmartResize(80, 80)], format='png')


    class Meta:
        abstract = True

# Local user profile. This could be filled using social signup
#
class UserProfile(AbstractProfile):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_profile', verbose_name=_('User'))
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def __unicode__(self):
        return u'{0}'.format(self.user)

    def __str__(self):
        return self.__unicode__()


class UserReferral(CreatedModifiedTimeModel):
    """
    User Referral Concrete Model.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_referral', verbose_name=_('User'))
    referrer = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='user_referrer',
                                 verbose_name=_('Referrer'), help_text=_('Optional'))
    referral = models.PositiveSmallIntegerField(choices=UserReferralChoices, verbose_name=_('Referral Type'))


    class Meta:
        verbose_name = _('Referral')
        verbose_name_plural = _('Referrals')

    def __unicode__(self):
        return u'{0}-{1}-{2}'.format(self.from_user, self.to_user, self.relationship)

    def __str__(self):
        return self.__unicode__()


class UserRelationship(PublishableModel):
    """
    User Relationship Concrete Model.
    """
    # # need confirmed_on, hash??

    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user_relation',
                                  verbose_name=_('From User'))
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user_relation', verbose_name=_('To User'))
    relationship = models.PositiveSmallIntegerField(choices=UserRelationshipChoices, verbose_name=_('Relationship'))
    confirmed = models.BooleanField(default=False, verbose_name=_('Confirmed by To User'))

    class Meta:
        verbose_name = _('Relation')
        verbose_name_plural = _('Relations')

    def __unicode__(self):
        return u'{0} : {1} - {2}'.format(UserRelationshipChoices[self.relationship], self.from_user, self.to_user)

    def __str__(self):
        return self.__unicode__()


# class UserProfile(ContactModel, SocialModel):
#     """
#     User Profile Model.
#     """
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_profile', verbose_name=_('User'))
#     biography = models.TextField(blank=True, null=True, verbose_name=_('Biography'))
#     birthday = models.DateField(blank=True, null=True, verbose_name=_('Date of Birth'))
#     designation = models.PositiveSmallIntegerField(choices=UserTitleChoices, blank=True, null=True,
#                                                    verbose_name=_('Designation'))
#     gender = models.PositiveSmallIntegerField(choices=UserGenderChoices, blank=True, null=True,
#                                               verbose_name=_('Gender'))
#     image = models.FileField(upload_to='users', max_length=2048, blank=True, verbose_name=_('Picture'))
#     thumbnail = ImageSpecField(source='image', processors=[SmartResize(80, 80)], format='png')
#     video = EmbedVideoField(blank=True, null=True, verbose_name=_('Video'))

#     class Meta:
#         verbose_name = _('User Profile')
#         verbose_name_plural = _('User Profiles')

#     def __unicode__(self):
#         return u'{0}'.format(self.user)

#     def __str__(self):
#         return self.__unicode__()


class UserSetting(CreatedModifiedTimeModel):
    """
    User Settings Model.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_setting', verbose_name=_('User'))
    receive_email_notifications = models.BooleanField(default=True, verbose_name=_('Receive Notifications?'))
    receive_newsletters = models.BooleanField(default=True, verbose_name=_('Receive Newsletters?'))
    visible_profile = models.BooleanField(default=True, verbose_name=_('Profile Visible?'))

    class Meta:
        verbose_name = _('User Setting')
        verbose_name_plural = _('User Settings')

    def __unicode__(self):
        return u'{0}'.format(self.user)

    def __str__(self):
        return self.__unicode__()
