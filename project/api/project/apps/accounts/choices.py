from django.utils.translation import ugettext_lazy as _

from model_utils import Choices

UserAccountTypeChoices = Choices(
    (1, 'Individual', _('Individual')),
    (2, 'Business', _('Business')),
)

UserTitleChoices = Choices(
    (1, 'Mr', _('Mr')),
    (2, 'Mrs', _('Mrs')),
    (3, 'Miss', _('Miss')),
    (4, 'Ms', _('Ms')),
    (5, 'Dr', _('Dr')),
    (6, 'Prof', _('Prof')),
    (7, 'Hon', _('Hon')),
)

UserGenderChoices = Choices(
    (1, 'Male', _('Male')),
    (2, 'Female', _('Female')),
    (3, 'Other', _('Do not want to specify')),
)

LoginChoices = Choices(
    (1, 'Facebook', _('Facebook')),
    (2, 'LinkedIn', _('LinkedIn')),
    (3, 'Django', _('Django')),
)

UserRelationshipChoices = Choices(
    (1, 'Follower', _('Follower')),
    (2, 'Colleague', _('Work Related')),
    (3, 'Friend', _('Friend')),
    (4, 'Acquaintance', _('Acquaintance')),
    (4, 'Stranger', _('I do not know this person')),
)

UserReferralChoices = Choices(
    (1, 'Friend', _('Friend / Relative')),
    (2, 'Work', _('Work / Colleague / Employer')),
    (3, 'Event', _('Event / Exhibition')),
    (4, 'TV', _('TV Advert')),
    (5, 'Radio', _('Local Radio')),
    (6, 'Newspaper', _('Newspaper Advert')),
    (7, 'Social', _('Facebook / LinkedIn / Twitter / Google+')),
    (8, 'Email', _('Personalised Email')),
    (9, 'Other', _('Other')),
)

