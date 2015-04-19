from django.utils.translation import ugettext_lazy as _

from model_utils import Choices


CourseTuitionLevelChoices = Choices(
    (1, 'Beginner', _('Beginner')),
    (2, 'Intermediate', _('Intermediate')),
    (3, 'Advanced', _('Advanced')),
)

CourseTuitionTypeChoices = Choices(
    (1, 'Online', _('Online/Distance learning')),
    (2, 'Classroom', _('Classroom')),
    (3, 'Onsite', _('On-Site')),
    (3, 'Apprenticeship', _('Apprenticeship')),
)

CourseTuitionPaymentChoices = Choices(
    (1, 'Hour', _('Hour')),
    (2, 'Day', _('Day')),
    (3, 'Month', _('Month')),
    (4, 'Year', _('Year')),
    (6, 'TBD', _('To Be Decided')),
)

QualificationChoices = Choices(
    (1, 'CPE', _('Certificate of Primary Education')),
    (2, 'SC', _('GCSE O\'Level / School Certificate')),
    (3, 'HSC', _('GCE A\' Level / Higher School Certificate')),
    (4, 'Dip', _('Diploma')),
    (5, 'AdvancedDip', _('Advanced Diploma')),
    (6, 'Deg', _('Degree')),
    (7, 'PostDeg', _('Postgraduate Degree')),
    (8, 'Doc', _('Doctorate')),
    (9, 'Other', _('Other')),
)

WorkSalaryChoices = Choices(
    (1, 'Hour', _('Hour')),
    (2, 'Day', _('Day')),
    (3, 'Month', _('Month')),
    (4, 'Year', _('Year')),
    (5, 'Project', _('Project')),
    (6, 'TBD', _('To Be Decided')),
)

WorkTypeChoices = Choices(
    (1, 'Full-Time', _('Full-Time')),
    (2, 'Part-Time', _('Part-Time')),
    (3, 'Freelance', _('Freelance')),
    (4, 'Internship', _('Internship')),
    (5, 'Volunteer', _('Volunteer')),
)

WorkEnvironmentChoices = Choices(
    (1, 'At Office', _('At Office')),
    (2, 'At Home', _('At Home')),
    (3, 'Travel a lot', _('Travel a lot')),
)

WorkExperienceChoices = Choices(
    (1, 'No Experience Required', _('No Experience Required')),
    (2, 'Intern', _('Intern / Apprentice')),
    (3, 'Junior', _('1 to 3 years')),
    (4, 'Professional', _('3 to 5 years')),
    (5, 'Senior', _('5 to 10 years')),
    (6, 'Expert', _('10+ years')),
)