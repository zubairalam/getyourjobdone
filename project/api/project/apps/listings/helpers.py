from decimal import Decimal

from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.translation import ugettext_lazy as _

from constance import config

from apps.core.helpers import generate_random_character_sequence
from .choices import WorkSalaryChoices


def generate_reference_number(contract, company):
    return 'JPS' + '-' + company[:2].upper() + contract[:3].upper() + '-' + generate_random_character_sequence(5)


def generate_salary_range(salary_frequency, salary_min, salary_max):
    salary_min = int(salary_min) if Decimal(salary_min) % 1 == 0 else '%.2f' % salary_min
    salary_max = int(salary_max) if Decimal(salary_max) % 1 == 0 else '%.2f' % salary_max
    rate = 'per {0}'.format(WorkSalaryChoices[salary_frequency].lower()) if salary_frequency else ''
    if salary_min == 0 == 0.00 and salary_max == 0 == 0.00:
        return 'Please Enquire.'
    elif salary_min == salary_max:
        return '{0} {1} {2}'.format(config.CURRENCY_SIGN, str(intcomma(salary_min)), rate)
    elif salary_min < salary_max:
        if salary_min == 0 == 0.00:
            return '{0} {1} {2}'.format(config.CURRENCY_SIGN, str(intcomma(salary_max)), rate)
        return '{0} {1} - {2} {3}'.format(config.CURRENCY_SIGN, str(intcomma(salary_min)), str(intcomma(salary_max)),
                                          rate)


# def get_start_work_time(self):
# if self.start_work_hour >= 0 and self.start_work_minutes >= 0:
#         return unicode(HourChoices[self.start_work_hour][1]).lower() + ':' + unicode(
#             MinuteChoices[self.start_work_minutes][1]).lower()
#
# def get_end_work_time(self):
#     if self.end_work_hour >= 0 and self.end_work_minutes >= 0:
#         return unicode(HourChoices[self.end_work_hour][1]).lower() + ':' + unicode(
#             MinuteChoices[self.end_work_minutes][1]).lower()
#
# def get_work_days(self):
#     regular_days = Day.objects.filter(pk__in=[1, 2, 3, 4, 5])
#     if str(regular_days) == str(self.work_days.all()):
#         return _('Monday to Friday')
#     return ''
