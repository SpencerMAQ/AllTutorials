import unittest
from collections.abc import (Container, Sized,
                             Iterable, Sequence, Set)

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

    # VID 15: Testing Protocol Implementations
    def test_protocols(self):
        self.assertTrue(issubclass(SortedSet, Container))



class TestSizedProtocol(unittest.TestCase):

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

    # VID 15: Test Protocols
    # from what I understand, if you implement the
    # abstract method listed here: https://docs.python.org/3.4/library/collections.abc.html
    # then you implement that protocol
    def test_sized_protocol(self):
        self.assertTrue(issubclass(SortedSet, Sized))

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

    def test_protocol(self):
        self.assertTrue(issubclass(SortedSet, Iterable))


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

    # ##### ===========
    # testing the reversed protocol
    def test_reversed(self):
        # note that if __reversed__ is implement
        # python uses that
        # if not, it uses both __getitem__ and __len__
        # instead. Python walks back through the sequence using the two
        s = SortedSet([1, 3, 5, 7])
        r = reversed(s)
        self.assertEqual(next(r), 7)
        self.assertEqual(next(r), 5)
        self.assertEqual(next(r), 3)
        self.assertEqual(next(r), 1)
        with self.assertRaises(StopIteration):
            next(r)

    # Vid 11: Sequence Protol - index(), count()

    # index of item exists
    def test_index_positive(self):
        s = SortedSet([1, 5, 8, 9])
        self.assertEqual(s.index(8), 2)

    def test_index_negative(self):
        s = SortedSet([1, 5, 8, 9])
        with self.assertRaises(ValueError):
            s.index(15)

    # VID 12: Checking that collections.abc Sequence
    # also implements count()
    def test_count_zero(self):
        s = SortedSet([1, 5, 5, 7, 9])
        self.assertEqual(s.count(11), 0)


    def test_count_one(self):
        s = SortedSet([1, 5, 5, 7, 9])
        self.assertEqual(s.count(9), 1)

    # with duplicates from declaration
    def test_count_dup_one(self):
        s = SortedSet([1, 5, 5, 7, 9])
        self.assertEqual(s.count(5), 1)

    def test_protocol(self):
        self.assertTrue(issubclass(SortedSet, Sequence))

    # VID 16: concatenation and repitition
    def test_concatenate_disjoin(self):
        s = SortedSet([1, 2, 3,])
        t = SortedSet([4, 5, 6,])
        self.assertEqual(s + t, SortedSet([1, 2, 3, 4, 5, 6]))

    def test_concatenate_equal(self):
        s = SortedSet([2, 4, 6])
        self.assertEqual(s + s, s)

    def test_concatenate_intersecting(self):
        s = SortedSet([1, 2, 3])
        t = SortedSet([3, 4, 5])
        self.assertEqual(s + t, SortedSet([1, 2, 3, 4, 5]))

    # Testing repitition
    # since this is a set, it doesn't make sense to
    # make duplicates of the members, so we simply
    # return the set itself unless the repitition is zero
    def test_repitition_zero_left(self):
        s = SortedSet([4, 5, 6])
        self.assertEqual(0 * s, SortedSet())

    def test_repitition_nonzero_left(self):
        s = SortedSet([4, 5, 6])
        self.assertEqual(100 * s, s)

    def test_repitition_zero_right(self):
        s = SortedSet([4, 5, 6])
        self.assertEqual(s * 0, SortedSet())

    def test_repitition_nonzero_right(self):
        s = SortedSet([4, 5, 6])
        self.assertEqual(s * 100, s)


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


class TestRelationalSetProtocol(unittest.TestCase):

    def test_lt_positive(self):
        s = SortedSet({1, 2})
        t = SortedSet({1, 2, 3})
        self.assertTrue(s < t)

    def test_lt_negative(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({1, 2, 3})
        self.assertFalse(s < t)

    def test_le_lt_positive(self):
        s = SortedSet({1, 2})
        t = SortedSet({1, 2, 3})
        self.assertTrue(s <= t)

    def test_le_eq_positive(self):
        s = SortedSet({1, 2})
        t = SortedSet({1, 2, 3})
        self.assertTrue(s <= t)

    def test_le_negative(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({1, 2})
        self.assertFalse(s <= t)

    def test_gt_positive(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({1, 2})
        self.assertTrue(s > t)

    def test_gt_negative(self):
        s = SortedSet({1, 2})
        t = SortedSet({1, 2, 3})
        self.assertFalse(s > t)

    def test_ge_gt_positive(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({1, 2})
        self.assertTrue(s >= t)

    def test_ge_eq_positive(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({1, 2, 3})
        self.assertTrue(s >= t)

    def test_ge_negative(self):
        s = SortedSet({1, 2})
        t = SortedSet({1, 2, 3})
        self.assertFalse(s >= t)


class TestRelationalMethods(unittest.TestCase):
    """
    for named methods as opposed to infix
    """
    def test_issubset_proper_positive(self):
        s = SortedSet({1, 2})
        t = [1, 2, 3]
        self.assertTrue(s.issubset(t))

    def test_issubset_positive(self):
        s = SortedSet({1, 2, 3})
        t = [1, 2, 3]
        self.assertTrue(s.issubset(t))

    def test_issubset_negative(self):
        s = SortedSet({1, 2, 3})
        t = [1, 2]
        self.assertFalse(s.issubset(t))

    def test_issuperset_proper_positive(self):
        s = SortedSet({1, 2, 3})
        t = [1, 2, 3]
        self.assertTrue(s.issuperset(t))

    def test_issuperset_positive(self):
        s = SortedSet({1, 2, 3})
        t = [1, 2, 3]
        self.assertTrue(s.issuperset(t))

    def test_issuperset_negative(self):
        s = SortedSet({1, 2})
        t = [1, 2, 3]
        self.assertFalse(s.issuperset(t))


class TestOperationsSetProtocol(unittest.TestCase):

    def test_intersection(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({2, 3, 4})
        self.assertEqual(s & t, SortedSet({2, 3}))

    def test_union(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({2, 3, 4})
        self.assertEqual(s | t, SortedSet({1, 2, 3, 4}))

    def test_symmetric_difference(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({2, 3, 4})
        self.assertEqual(s ^ t, SortedSet({1, 4}))

    def test_difference(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({2, 3, 4})
        self.assertEqual(s - t, SortedSet({1}))


class TestSetOperationsMethods(unittest.TestCase):

    def test_intersection(self):
        s = SortedSet({1, 2, 3})
        t = [2, 3, 4]
        self.assertEqual(s.intersection(t), SortedSet({2, 3}))

    def test_union(self):
        s = SortedSet({1, 2, 3})
        t = [2, 3, 4]
        self.assertEqual(s.union(t), SortedSet({1, 2, 3, 4}))

    def test_symmetric_diff(self):
        s = SortedSet({1, 2, 3})
        t = [2, 3, 4]
        self.assertEqual(s.symmetric_difference(t), SortedSet({1, 4}))

    def test_difference(self):
        s = SortedSet({1, 2, 3})
        t = [2, 3, 4]
        self.assertEqual(s.difference(t), SortedSet({1}))

    # test isdisjoin()
    def test_isdisjoint_postitive(self):
        s = SortedSet([1, 2 ,3])
        t = [4, 5, 6]
        self.assertTrue(s.isdisjoint(t))

    def test_isdisjoint_negative(self):
        s = SortedSet([1, 2 ,3])
        t = [3, 4, 5]
        self.assertFalse(s.isdisjoint(t))

# Vid 17: Finally, ascertain that we've implemented the set protocol

class TestSetProtocol(unittest.TestCase):

    def test_protocol(self):
        self.assertTrue(issubclass(SortedSet, Set))

if __name__ == '__main__':
    unittest.main()
