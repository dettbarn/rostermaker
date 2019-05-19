import unittest

import priorities as p
import exceptions as e


class TestPriorities(unittest.TestCase):

    def test_init(self):
        prio = p.Priorities()
        # prio.dict should be initialized empty, but do exist
        self.assertTrue(bool(prio))
        self.assertFalse(bool(prio.dict))

    def test_setdict(self):
        d = {"a": 3, "c": 5, "b": 7}
        prio = p.Priorities()
        prio.setdict(d)
        self.assertEqual(d, prio.dict)

    def test_setweight(self):
        prio = p.Priorities()
        prio.setweight("apples", 10)
        self.assertEqual(prio.dict["apples"], 10)
        prio.setweight("apples", 38)
        self.assertEqual(prio.dict["apples"], 38)
        prio.setweight("pears", 38)
        self.assertEqual(prio.dict["apples"], 38)
        self.assertEqual(prio.dict["pears"], 38)

    def test_scaleweight(self):
        prio = p.Priorities()
        prio.setweight("apples", 7)
        prio.setweight("pears", 2)
        self.assertEqual(prio.dict["apples"], 7)
        self.assertEqual(prio.dict["pears"], 2)
        prio.scaleweight("apples", 3)
        self.assertEqual(prio.dict["apples"], 21)
        self.assertEqual(prio.dict["pears"], 2)
        prio.scaleweight("bananas", 4.1)
        self.assertEqual(prio.dict["bananas"], 4.1)
        self.assertRaises(e.IllegalNegativeException, prio.scaleweight, "pears", -2)

    def test_getweight(self):
        prio = p.Priorities()
        prio.setweight("some", 3)
        self.assertEqual(prio.getweight("some"), 3)
        prio.scaleweight("some", 2)
        self.assertEqual(prio.getweight("some"), 6)
        self.assertRaises(e.IllegalNegativeException, prio.scaleweight, "some", -2)
        self.assertEqual(prio.getweight("some"), 6)

    def test_isempty(self):
        prio = p.Priorities()
        self.assertFalse(bool(prio.dict))
        self.assertEqual(len(prio.dict), 0)
        self.assertTrue(prio.isempty())
        prio.setweight("apples", 7)
        self.assertTrue(bool(prio.dict))
        self.assertEqual(len(prio.dict), 1)
        self.assertFalse(prio.isempty())

    def test_max(self):
        prio = p.Priorities()
        prio.setdict({"a": 2, "b": 4, "c": 7})
        self.assertEqual(prio.max(), 7)
        prio.scaleweight("c", 0.2)
        self.assertEqual(prio.max(), 4)
        prio.scaleweight("a", 5)
        self.assertEqual(prio.max(), 10)

    def test_min(self):
        prio = p.Priorities()
        prio.setdict({"a": 2, "b": 4, "c": 10})
        self.assertEqual(prio.min(), 2)
        prio.scaleweight("a", 5)
        self.assertEqual(prio.min(), 4)
        prio.scaleweight("c", 0.2)
        self.assertEqual(prio.min(), 2)

    if __name__ == '__main__':
        unittest.main()
