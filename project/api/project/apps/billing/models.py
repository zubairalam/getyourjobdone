from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from apps.core.models import ContentModel, CreatedModifiedTimeModel, CreatedExpiredModifiedTimeModel, PayableModel, \
    PublishableModel
from apps.accounts.choices import UserAccountTypeChoices
from apps.accounts.models import UserAccount
from .choices import PackageTypeChoices


class UserCredit(ContentModel):
    pass


class Feature(ContentModel):
    """
    Feature Abstract Model.
    """
    icon = models.URLField(blank=True, null=True, verbose_name=_('Icon'))

    class Meta:
        verbose_name = _('Feature')
        verbose_name_plural = _('Features')


# # title = Individual Starter
## description = Earn money
## features = 10 jobs, feature your picture on homepage, 30 days == 10 J / 30 days, 1 Profile F / 10 days


## title = Business Starter
## description = Blah Blah
## features = 10 Jobs Post / 90 days, 200 UserProfile access.


class Package(ContentModel, PublishableModel):
    """
    Package Concrete Model.
    """
    account_type = models.PositiveSmallIntegerField(choices=UserAccountTypeChoices, verbose_name=_('Applies to'))
    category = models.PositiveIntegerField(choices=PackageTypeChoices, verbose_name=_('Category'))
    features = models.ManyToManyField(Feature, verbose_name=_('Package Features'))
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name=_('Cost'))


    class Meta:
        verbose_name = _('Package')
        verbose_name_plural = _('Packages')


class Subscription(CreatedExpiredModifiedTimeModel):
    """
    Subscription Concrete Model.
    """
    account = models.ForeignKey(UserAccount, verbose_name=_('Account'))
    package = models.ForeignKey(Package, verbose_name=_('Package'))
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name=_('Price'))

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')


    def __unicode__(self):
        return u'{0}-{1}'.format(self.account, self.package)

    def __str__(self):
        return self.__unicode__()


class Transaction(CreatedModifiedTimeModel, PayableModel):
    """
    Transaction Concrete Model.
    """
    account = models.ForeignKey(UserAccount, verbose_name=_('Account'))
    payee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transaction_from_user', verbose_name=_('Payee'))

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')


    def __unicode__(self):
        return u'{0}-{1}-{2}-{3}'.format(self.payment_status, self.payee, self.amount, self.created)


    def __str__(self):
        return self.__unicode__()