import unittest

from roster import Roster
from functions import ndays


class TestRoster(unittest.TestCase):

    def test_init(self):
        nshiftsperday = 3
        qualified = ["Q1", "Q2", "Q3"]
        regular = ["R1", "R2", "R3", "R4", "R5"]
        monthno = 5
        year = 2019
        roster = Roster(nshiftsperday, qualified, regular, monthno, year)
        self.assertEqual(roster.nshiftsperday, nshiftsperday)
        self.assertEqual(roster.qualified, qualified)
        self.assertEqual(roster.regular, regular)
        self.assertEqual(roster.monthno, monthno)
        self.assertEqual(roster.year, year)
        self.assertEqual(roster.ndays, ndays(monthno, year))
        self.assertEqual(len(roster.arr), ndays(monthno, year))
        self.assertEqual(len(roster.arr[0]), nshiftsperday)
        for iday in range(0, roster.ndays):
            for ishift in range(0, roster.nshiftsperday):
                self.assertEqual(roster.arr[iday][ishift], "")

    if __name__ == '__main__':
        unittest.main()
