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


class TestSizeProtocol(unittest.TestCase):

    # there are only 3 interesting number in
    # com sci, 0, 1 and n
    def test_empty(self):
        s = SortedSet()
        self.assertEqual(len(s), 0)

    def test_one(self):
        s = SortedSet([33])
        self.assertEqual(len(s), 1)

    def test_ten(self):
        s = SortedSet(range(10))
        self.assertEqual(len(s), 10)

    # will fail if duplicates are not removed
    def test_with_duplicates(self):
        s = SortedSet([5, 5, 5, 5, 5])
        self.assertEqual(len(s), 1)

class TestIterableProtocol(unittest.TestCase):

    def setUp(self):
        self.s = SortedSet([7, 2, 1, 3, 1, 20])
        # expected: 1, 2, 3, 7, 20

    def test_iter(self):
        i = iter(self.s)
        # if the Collection does sort, then 1 should
        # be next
        self.assertEqual(next(i), 1)
        self.assertEqual(next(i), 2)
        self.assertEqual(next(i), 3)
        self.assertEqual(next(i), 7)
        self.assertEqual(next(i), 20)
        # lambda
        # This is so that the assertion calls next(i) rather than
        # our code calling next(i) and passing the result of that
        # to the assertion
        self.assertRaises(StopIteration, lambda: next(i))

    def test_for_loop(self):
        # expected: 1, 2, 3, 7, 20
        index = 0
        expected = [1, 2, 3, 7, 20]
        # for item in self.s:
        #     self.assertEqual(item, expected[index])
        #     index += 1
        for i, item in enumerate(self.s):
            self.assertEqual(item, expected[i])


class TestSequenceProtocol(unittest.TestCase):
    # First, indexing and slicing through __getitem__

    def setUp(self):
        self.s = SortedSet([1, 4, 9, 13, 15])

    def test_index_zero(self):
        self.assertEqual(self.s[0], 1)

    def test_index_four(self):
        self.assertEqual(self.s[4], 15)

    def test_index_beyond_scope(self):
        with self.assertRaises(IndexError):
            self.s[5]

    def test_index_minus_one(self):
        self.assertEqual(self.s[-1], 15)

    def test_index_minus_five(self):
        self.assertEqual(self.s[-5], 1)


    def test_index_one_before_the_beginning(self):
        # TODO: how does this work?
        with self.assertRaises(IndexError):
            self.s[-6]

    # Tests for Slicing
    # Notice that writing these tests drives us to a DESIGN DECISION
    # that slicing a SortedSet should return a SortedSet, not a list, or any
    # unordered, unsorted collection

    # By default(before vid 7, the slices return a list)
    # To change this behavior, would need a more sophisticated __getitem__
    # that detects whether it's being called with an index or a slice
    # and acts accordingly
    def test_slice_from_start(self):
        self.assertEqual(self.s[:3], SortedSet([1, 4, 9]))

    def test_slice_to_end(self):
        self.assertEqual(self.s[3:], SortedSet([13, 15]))

    def test_slice_empty(self):
        self.assertEqual(self.s[10:], SortedSet())

    def test_slice_arbitrary(self):
        self.assertEqual(self.s[2:4], SortedSet([9, 13]))

    def test_slice_full(self):
        self.assertEqual(self.s[:], self.s)
    # unittest would still have problems like
    # SortedSet([1, 2]) != SortedSet([1, 2])
    # that is because by default, python equality comparison (==) inherits from
    # object, which is for REFERENCE equality i.e. 'is', are they the same object?

    # In fact this is the default behavior for all objects in python
    # unless == was specialized by the object
    # i.e. by default == and 'is' are the same

    # to override that, we must override ==


class TestReprProtocol(unittest.TestCase):

    def test_repr_empty(self):
        s = SortedSet()
        self.assertEqual(repr(s), 'SortedSet()')

    def test_repr_some(self):
        s = SortedSet([42, 40, 19])
        self.assertEqual(repr(s), 'SortedSet([19, 40, 42])')


class TestEqualityProtocol(unittest.TestCase):

    def test_positive_equal(self):
        self.assertTrue(SortedSet([4, 5, 6]) == SortedSet([6, 5, 4]))

    def test_negative_equal(self):
        self.assertFalse(SortedSet([4, 5, 6]) == SortedSet([1, 2, 3]))

    # object vs typical list
    def test_type_mismatch(self):
        self.assertFalse(SortedSet([4, 5, 6]) == [4, 5, 6])

    # sanity check to make sure SortedSet() is equal to itself
    def test_identical(self):
        s = SortedSet([10, 11 ,12])
        self.assertTrue(s == s)


class TestInequalityProtocol(unittest.TestCase):
    """
    Note that in this case, we use != on all cases
    regardless of the double negative
    """

    # note that these tests are passing by default
    # indicating that python implements != by negating ==

    # although that is the case, it is best practice to define __ne__
    # as per python documentation because they are not nec. inverse
    def Test_positive_unequal(self):
        self.assertTrue(SortedSet([4, 5, 6]) != SortedSet([1, 2, 3]))

    def Test_negative_unequal(self):
        self.assertFalse(SortedSet([4, 5, 6]) != SortedSet([6, 5, 4]))

    def Test_type_mismatch(self):
        self.assertTrue(SortedSet([4, 5, 6]) != [1, 2, 3])

    def Test_identical(self):
        s = SortedSet([])
        self.assertFalse(s != s)

if __name__ == '__main__':
    unittest.main()