import unittest

from sorted_set import SortedSet

class TestConstruction(unittest.TestCase):

    def test_empty(self):
        s = SortedSet([])

    def test_from_sequence(self):
        s = SortedSet([1,2,3,4])

    def test_with_duplicates(self):
        s = SortedSet([8,8,8])

    def test_from_iterable(self):
        def gen684():
            yield 6
            yield 8
            yield 1
            yield 10
        g = gen684()
        s = SortedSet(g)

    def test_default_empty(self):
        s = SortedSet()


class TestContainerProtocol(unittest.TestCase):
    def setUp(self):
        self.s = SortedSet([6,7,8,9])

    def test_positive_contained(self):
        self.assertTrue(6 in self.s)

    def test_negative_contained(self):
        self.assertFalse(2 in self.s)

    def test_positive_not_contained(self):
        self.assertTrue(5 not in self.s)

    def test_negative_not_contained(self):
        self.assertFalse(9 not in self.s)

if __name__ == '__main__':
    unittest.main()