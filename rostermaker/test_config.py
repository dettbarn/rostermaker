import unittest

from config import Config
import restrictions as re


class TestConfig(unittest.TestCase):

    def test_write_read(self):
        conf = Config()
        conf.setdefault()
        conf.setqualified(["A", "B", "C"])
        conf.setregular(["a", "b", "c", "d"])
        conf.setmonth(1)
        conf.setyear(2001)
        conf.setmonthstartswith(3)
        conf.setvacation("A", [1, 2, 3])
        restr = re.Restrictions()
        restr._setall([3, 1, 10, 1, 0, 1, 6, 3, 7, 1, 2, 3])
        conf.setrestrictions(restr.dict)
        filename = "./testconf.out"
        conf.writetofile(filename)
        conf2 = Config.setfromfile(filename)
        filename2 = "./testconf2.out"
        conf2.writetofile(filename2)
        self.assertEqual(conf, conf2)

    if __name__ == '__main__':
        unittest.main()
