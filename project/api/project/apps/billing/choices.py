from django.utils.translation import ugettext_lazy as _

from model_utils import Choices

PackageTypeChoices = Choices(
    (1, 'PAYG', _('Pay as you go')),
    (2, 'Monthly', _('Monthly')),
    (3, 'Annual', _('Annual')),
    (4, 'Custom', _('Custom')),
)

