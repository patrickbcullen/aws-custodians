from unittest import TestCase
from custodians.util import flatten_dict, age_in_days
from datetime import datetime

def _datetime(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')

class UtilTest(TestCase):
    def test_age_in_days(self):
        reference_date = _datetime('2016-01-01')
        now = _datetime('2016-01-02')
        self.assertEquals(1, age_in_days(reference_date, now=now))

    def test_flatten_dict(self):
        reference_dict = {'A': 'B'}
        self.assertEquals("A='B'", flatten_dict(reference_dict))
