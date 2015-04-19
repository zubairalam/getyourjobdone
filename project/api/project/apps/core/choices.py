from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices

from .helpers import make_tuple

CURRENT_DAY = timezone.now().day
CURRENT_MONTH = timezone.now().month
CURRENT_YEAR = timezone.now().year
YearChoices = (
    map(make_tuple, range(1900, CURRENT_YEAR + 5))
)

DayChoices = Choices(
    (1, 'Monday', _('Monday')),
    (2, 'Tuesday', _('Tuesday')),
    (3, 'Wednesday', _('Wednesday')),
    (4, 'Thursday', _('Thursday')),
    (5, 'Friday', _('Friday')),
    (6, 'Saturday', _('Saturday')),
    (7, 'Sunday', _('Sunday')),
)
MonthChoices = Choices(
    (1, 'January', _('January')),
    (2, 'February', _('February')),
    (3, 'March', _('March')),
    (4, 'April', _('April')),
    (5, 'May', _('May')),
    (6, 'June', _('June')),
    (7, 'July', _('July')),
    (8, 'August', _('August')),
    (9, 'September', _('September')),
    (10, 'October', _('October')),
    (11, 'November', _('November')),
    (12, 'December', _('December')),
)
DayTimeChoices = Choices(
    (1, 'Morning', _('am')),
    (2, 'Evening', _('pm')),
)

CalendarChoices = Choices(
    (1, 'Hour', _('Hour')),
    (2, 'Day', _('Day')),
    (3, 'Week', _('Week')),
    (4, 'Month', _('Month')),
    (5, 'Year', _('Year')),
)


# MonthDayChoices = (
# map(make_tuple, range(0, 31))
# )

MonthDayChoices = Choices(
    (1, '01', _('1st')),
    (2, '02', _('2nd')),
    (3, '03', _('3rd')),
    (4, '04', _('4th')),
    (5, '05', _('5th')),
    (6, '06', _('6th')),
    (7, '07', _('7th')),
    (8, '08', _('8th')),
    (9, '09', _('9th')),
    (10, '10', _('10th')),
    (11, '11', _('11th')),
    (12, '12', _('12th')),
    (13, '13', _('13th')),
    (14, '14', _('14th')),
    (15, '15', _('15th')),
    (16, '16', _('16th')),
    (17, '17', _('17th')),
    (18, '18', _('18th')),
    (19, '19', _('19th')),
    (20, '20', _('20th')),
    (21, '21', _('21th')),
    (22, '22', _('22nd')),
    (23, '23', _('23rd')),
    (24, '24', _('24th')),
    (25, '25', _('25th')),
    (26, '26', _('26th')),
    (27, '27', _('27th')),
    (28, '28', _('28th')),
    (29, '29', _('29th')),
    (30, '29', _('30th')),
    (31, '31', _('31st')),
)

HourChoices = Choices(
    (1, '00', _('00')),
    (2, '01', _('01')),
    (3, '02', _('02')),
    (4, '03', _('03')),
    (5, '04', _('04')),
    (6, '05', _('05')),
    (7, '06', _('06')),
    (8, '07', _('07')),
    (9, '08', _('08')),
    (10, '09', _('09')),
    (11, '10', _('10')),
    (12, '11', _('11')),
    (13, '12', _('12')),
    (14, '13', _('13')),
    (15, '14', _('14')),
    (16, '15', _('15')),
    (17, '16', _('16')),
    (18, '17', _('17')),
    (19, '18', _('18')),
    (20, '19', _('19')),
    (21, '20', _('20')),
    (22, '21', _('21')),
    (23, '22', _('22')),
    (24, '23', _('23')),
)

MinuteChoices = Choices(
    (1, '00', _('00')),
    (2, '15', _('15')),
    (3, '30', _('30')),
    (4, '45', _('45')),
)