import unittest

exec(compile(open("functions.py", "rb").read(), "functions.py", 'exec'))

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

if __name__ == '__main__':
    unittest.main()
