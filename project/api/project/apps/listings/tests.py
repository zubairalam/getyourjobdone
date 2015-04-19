from django.test import TestCase

from apps.jobs.choices import SalaryChoices
from apps.jobs.helpers import generate_salary_range, generate_reference_number


class ReferenceTest(TestCase):
    """
    This helps in testing job references for a job model.
    """

    def test_length(self):
        """
        Test the length of the job reference.
        """
        self.assertEquals(len(generate_reference_number('Permanent', 'XeonTek')), 15)
        self.assertEquals(len(generate_reference_number('Contract', 'XeonTek')), 16)
        self.assertEquals(len(generate_reference_number('Temporary', 'XeonTek')), 16)

    def test_randomness(self):
        '''
        Test the randomness of each job reference being generated.
        '''
        first_perm_ref = generate_reference_number('Permanent', 'XeonTek')
        second_perm_ref = generate_reference_number('Permanent', 'XeonTek')
        first_con_ref = generate_reference_number('Contract', 'XeonTek')
        second_con_ref = generate_reference_number('Contract', 'XeonTek')
        first_hour_ref = generate_reference_number('Temporary', 'XeonTek')
        second_hour_ref = generate_reference_number('Temporary', 'XeonTek')
        self.assertNotEquals(first_perm_ref, second_perm_ref)
        self.assertNotEquals(first_con_ref, second_con_ref)
        self.assertNotEquals(first_hour_ref, second_hour_ref)


class SalaryTest(TestCase):
    """
    This helps in testing salary ranges for a job model
    """

    def test_range(self):
        """
        Test the salary range if it matches the values being input.
        """
        self.assertEqual(generate_salary_range(SalaryChoices.Hour, 0, 0), 'Please Enquire.')
        self.assertEqual(generate_salary_range(SalaryChoices.Day, 0, 0.00), 'Please Enquire.')
        self.assertEqual(generate_salary_range(SalaryChoices.Month, 0.00, 0), 'Please Enquire.')
        self.assertEqual(generate_salary_range(SalaryChoices.OneOff, 0.00, 0.00), 'Please Enquire.')
        self.assertEqual(generate_salary_range(SalaryChoices.Hour, 0, 300), 'Rs. 300 per hour')
        self.assertEqual(generate_salary_range(SalaryChoices.Day, 500, 700), 'Rs. 500 - 700 per day')
        self.assertEqual(generate_salary_range(SalaryChoices.Day, 100, 1275.50), 'Rs. 100 - 1,275.50 per day')
        self.assertEqual(generate_salary_range(SalaryChoices.Day, 0, 1275.50), 'Rs. 1,275.50 per day')

