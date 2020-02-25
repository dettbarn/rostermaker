import unittest
import os
import glob

from roster import Roster
from functions import ndays
from config import Config
import restrictions as re


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
        return roster

    def test_setgetvac(self):
        ro = self.test_init()
        empl = "Q2"
        vacstr = "4,5,6"
        difvacstr = "7,8,9"
        ro.setvacation(empl, vacstr)
        self.assertEqual(ro.getvacation(empl), vacstr)
        self.assertNotEqual(ro.getvacation(empl), difvacstr)

    def test_setvacations(self):
        ro = self.test_init()
        empl1 = "Q2"
        vac1 = "4,5,6"
        empl2 = "R1"
        vac2 = "13,14,15"
        emplnovac = "R2"
        vacations = {empl1: vac1, empl2: vac2}
        ro.setvacations(vacations)
        self.assertEqual(ro.getvacation(empl1), vac1)
        self.assertEqual(ro.getvacation(empl2), vac2)
        self.assertEqual(ro.getvacation(emplnovac), "")
        self.assertNotEqual(ro.getvacation(empl1), vac2)
        self.assertNotEqual(ro.getvacation(empl1), "")
        self.assertNotEqual(ro.getvacation(empl2), vac1)
        self.assertNotEqual(ro.getvacation(empl2), "")
        self.assertNotEqual(ro.getvacation(emplnovac), vac1)
        self.assertNotEqual(ro.getvacation(emplnovac), vac2)

    def test_makeempty(self):
        roster = self.test_init()
        for iday in range(0, roster.ndays):
            for ishift in range(0, roster.nshiftsperday):
                roster.arr[iday][ishift] = "_".join(["foo",
                                                     str(iday), str(ishift)])
        roster.makeempty()
        for iday in range(0, roster.ndays):
            for ishift in range(0, roster.nshiftsperday):
                self.assertEqual(roster.arr[iday][ishift], "")

    def test_exportfull(self):
        roster = self.test_init()
        roster.setconf(self.testprep_confobj())
        tmpfolder = "./tmp"
        pref = "temptestexport"
        if os.path.exists(tmpfolder):
            raise Exception("Error: temporary folder already exists.")
            return -1
        os.mkdir(tmpfolder)
        roster.exportfull(pref, tmpfolder)
        notsupported = ["bmp", "mp4", "ogg"]
        for format in notsupported:
            for file in glob.glob(tmpfolder + "/" + pref + "*." + format):
                assertRaises(os.remove, file)
        for format in Roster.supportedformats:
            for file in glob.glob(tmpfolder + "/" + pref + "*." + format):
                os.remove(file)
        os.rmdir(tmpfolder)

    def testprep_confobj(self):
        conf = Config()
        conf.setdefault()
        conf.setqualified(["A", "B", "C", "D", "E", "F", "G"])
        conf.setregular(["a", "b", "c", "d", "e", "f", "g", "h", "i"])
        conf.setmonth(1)
        conf.setyear(2001)
        restr = re.Restrictions()
        restr._setall([3, 1, 10, 1, 0, 1, 6, 3, 7, 1, 2, 3])
        conf.setrestrictions(restr.dict)
        conf.setlanguage('en')
        return conf

    def test_tryfill(self):
        ro1 = self.test_init()
        ro2 = ro1
        ro2.setconf(self.testprep_confobj())
        ro2.tryfill()
        # tryfill should only fill the arr, nothing else
        self.assertEqual(ro1.qualified, ro2.qualified)
        self.assertEqual(ro1.regular, ro2.regular)
        self.assertEqual(ro1.monthno, ro2.monthno)
        self.assertEqual(ro1.year, ro2.year)
        self.assertEqual(ro1.ndays, ro2.ndays)
        self.assertEqual(ro1.arrvacqualified, ro2.arrvacqualified)
        self.assertEqual(ro1.arrvacregular, ro2.arrvacregular)
        self.assertEqual(len(ro1.arr), len(ro2.arr))
        self.assertEqual(len(ro1.arr[0]), len(ro2.arr[0]))

    if __name__ == '__main__':
        unittest.main()
