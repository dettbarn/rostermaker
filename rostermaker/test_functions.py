import unittest

from functions import twodigit, isleapyear, ndays


class TestFunctions(unittest.TestCase):

    def test_twodigit(self):
        self.assertEqual(twodigit(7), "07")
        self.assertEqual(twodigit(42), "42")
        self.assertEqual(twodigit(0), "00")
        self.assertEqual(twodigit(-1), "01")
        self.assertEqual(twodigit(-42), "42")
        self.assertEqual(twodigit(100), "00")

    def test_isleapyear(self):
        self.assertTrue(isleapyear(4))
        self.assertTrue(isleapyear(16))
        self.assertTrue(isleapyear(400))
        self.assertTrue(isleapyear(2000))
        self.assertTrue(isleapyear(1992))
        self.assertFalse(isleapyear(13))
        self.assertFalse(isleapyear(15))
        self.assertFalse(isleapyear(100))
        self.assertFalse(isleapyear(1900))
        self.assertFalse(isleapyear(2100))
        self.assertFalse(isleapyear(2019))

    def test_ndays(self):
        noLeapYears = [42, 69, 1337, 1700, 1900, 2001, 2002, 2003]
        LeapYears = [4, 12, 644, 2000, 2004, 2008, 2400]
        for year in (noLeapYears + LeapYears):
            self.assertEqual(ndays(1, year), 31)
            self.assertEqual(ndays(3, year), 31)
            self.assertEqual(ndays(4, year), 30)
            self.assertEqual(ndays(5, year), 31)
            self.assertEqual(ndays(6, year), 30)
            self.assertEqual(ndays(7, year), 31)
            self.assertEqual(ndays(8, year), 31)
            self.assertEqual(ndays(9, year), 30)
            self.assertEqual(ndays(10, year), 31)
            self.assertEqual(ndays(11, year), 30)
            self.assertEqual(ndays(12, year), 31)
        for year in noLeapYears:
            self.assertEqual(ndays(2, year), 28)
        for year in LeapYears:
            self.assertEqual(ndays(2, year), 29)

    if __name__ == '__main__':
        unittest.main()
