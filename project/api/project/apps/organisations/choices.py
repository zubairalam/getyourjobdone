from django.utils.translation import ugettext_lazy as _

from model_utils import Choices


OrganisationTypes = Choices(
    (1, 'Private', _('Private Company')),
    (2, 'Public', _('Public Company')),
    (3, 'University', _('University')),
    (4, 'School', _('School')),
    (5, 'College', _('College')),
    (6, 'Training', _('Training Institute')),
    (7, 'Government', _('Government Body')),
)

OrganisationWorkForce = Choices(
    (1, 'Micro', _('1 to 4')),
    (2, 'Mini', _('5 to 9')),
    (3, 'Small', _('10 to 24')),
    (4, 'Large', _('25 to 99')),
    (5, 'Mega', _('100 to 999')),
    (6, 'Jumbo', _('1000+')),
)

