import unittest
import gettext

try:
    exec(compile(open("input", "rb").read(), "input", 'exec'))
except FileNotFoundError:
    print("No input file found.")

_ = gettext.gettext

from functions import isinshift, addtoshift
from functions import isshiftchange, weightedrnd, daystr
from functions import emptyarr, monthstr
from functions import twodigit, isleapyear, ndays
import exceptions as e
from config import Config



class TestFunctions(unittest.TestCase):

    # test preparation function
    # returns a somewhat default config object to be used for test functions
    def testprep_confobj(self):
        conf = Config()
        conf.setdefault()
        conf.str_sep = ','
        return conf

    def test_isinshift(self):
        conf = self.testprep_confobj()
        self.assertTrue(isinshift("Eric", "Stan,Kyle,Eric,Kenny", conf))
        self.assertTrue(isinshift("Tina", "Louise,Gene,Tina", conf))
        self.assertTrue(isinshift("Hayley", "Hayley,Steve,Roger,Klaus", conf))
        self.assertFalse(isinshift("Bart", "Fry,Leela,Zoidberg", conf))
        self.assertFalse(isinshift("Stewie", "Hero,Toot,Wooldoor", conf))
        self.assertFalse(isinshift("wRoNgCaSe", "wrongcase,Wrongcase", conf))
        self.assertFalse(isinshift("sym_bols", "Symbols,symbols", conf))

    def test_addtoshift(self):
        conf = self.testprep_confobj()
        self.assertEqual(addtoshift("First", "", conf), "First")
        self.assertEqual(addtoshift("Second", "First", conf), "First,Second")
        fin = "First,Second,Third"
        self.assertEqual(addtoshift("Third", "First,Second", conf), fin)

    def test_emptyarr(self):
        b = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.assertEqual(emptyarr(3, 3), b)
        b = [["", "", ""], ["", "", ""], ["", ""]]
        self.assertNotEqual(emptyarr(3, 3), b)
        b = [["", "", "", ""], ["", "", "", ""]]
        self.assertEqual(emptyarr(2, 4), b)
        b = [["", ""], ["", ""], ["", ""], ["", ""]]
        self.assertEqual(emptyarr(4, 2), b)

    def test_isshiftchange(self):
        conf = self.testprep_confobj()
        self.assertTrue(isshiftchange(conf.shiftnames[0], conf.shiftnames[1], conf))
        self.assertFalse(isshiftchange(conf.shiftnames[0], 'undef', conf))
        self.assertFalse(isshiftchange('undef', conf.shiftnames[0], conf))
        self.assertFalse(isshiftchange('undef', 'undef', conf))

    def test_weightedrnd(self):
        self.assertEqual(weightedrnd([0,42]),1)
        self.assertEqual(weightedrnd([41,0]),0)
        self.assertEqual(weightedrnd([0,0,0,0,42,0,0]),4)
        exc = e.AllWeightsZeroException
        self.assertRaises(exc, weightedrnd, [0,0,0])

    def test_daystr(self):
        self.assertEqual(daystr(0)," 0")
        self.assertEqual(daystr(3)," 3")
        self.assertEqual(daystr(9)," 9")
        self.assertEqual(daystr(10),"10")
        self.assertEqual(daystr(30),"30")

    def test_twodigit(self):
        self.assertEqual(twodigit(7), "07")
        self.assertEqual(twodigit(42), "42")
        self.assertEqual(twodigit(0), "00")
        self.assertEqual(twodigit(-1), "01")
        self.assertEqual(twodigit(-42), "42")
        self.assertEqual(twodigit(100), "00")

    def test_monthstr(self):
        self.assertEqual(monthstr(1),"January")
        self.assertEqual(monthstr(9),"September")
        exc = e.IllegalMonthException
        for illmo in [0, 13, -3, 1.5, 2.2]:
            self.assertRaises(exc, monthstr, illmo)

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