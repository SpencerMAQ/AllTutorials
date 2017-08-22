from bisect import bisect_left
from collections.abc import Sequence
"""
In principle, we could already implement
index() based on methods already in place
such as __getitem__

# https://docs.python.org/3.4/library/collections.abc.html
That's not needed however since 
Such default implementations are available in the py standard library
Just check the base classes of the collections.abc module
i.e. Container, Hashable, Iterable, SEQUENCE, etc.
abc = abstract base class

They serve to take some of the legwork of the collection protol implementation

Note from the docs that if you've already implemented
__getitem__ and __len__, contains, iter, reversed, index and count
are MIXIN method unless overridden
"""


class SortedSet(Sequence):
    """
    Only unique elements but ordered unlike a set
    """
    def __init__(self, items=None):
        # Note that sorted() always returns a list, this class acts like a set but
        # is essentially a class that creates a list-like object
        self._items = sorted(set(items)) if items is not None else []

    # container protocl "in"
    # without defining the iterable protocol
    # unittest would return four errors

    def __contains__(self, item):
        # return item in self._items
        # VID 14: notice that:
        # that found represents exactly the same result from __getitem__ (return item in self._items)
        #     found = (index != len(self._items) and (self._items[index] == value))
        # because of that, we replace the code in __contains__ to make it more efficient
        index = bisect_left(self._items, item)
        return index != len(self._items) and self._items[index] == item


    # sized protocol
    def __len__(self):
        return len(self._items)

    # iterable protocol
    # iterable = object where you can use iter() on
    def __iter__(self):
        # you can also use the generator form
        return iter(self._items)

    # sequence protol
    # 1. the object mmust be iterable, sized container
    # elements access using square brackets
    # slicing, reversed()
    # seq.index(item)
    # seq.count(item)
    # concatenation with + and *
    def __getitem__(self, item):
        result = self._items[item]
        # Tests for seeing what item is containing
        # when a slice is called on it, instead of an index
        print(item)
        property(type(item))
        # > would return things like
        # .slice(2, 4, None)
        # Fslice(10, 9329392392392329329, None)
        # <type slice>

        # It's logical that you'd wan't slice object to return
        # SortedSet object instead of generic lists
        return SortedSet(result) if isinstance(item, slice) else result

    # The string rep of this class for debugging is basically garbage
    # so you'd have to implement this for more info
    def __repr__(self):
        return 'SortedSet({})'.format(
            repr(self._items) if self._items else ''
        )

    # specialize == (eqaulity operator)
    # this is to ovverride the default setting that python
    # == is the same as 'is', i.e. identity test rather than content
    def __eq__(self, other):
        # NOTE: do note however that test_type_mismatch still fails
        # i.e. self.assertFalse(SortedSet([4, 5, 6]) == [4, 5, 6])
        # return self._items == other._items

        # a better implementation would be like this
        # i.e. typechecking first, returning the special builtin singleton
        # value not implemented if the types don't match
        if not isinstance(other, SortedSet):
            # notice that we return a NotImp object rather than
            # raising a NotImplementedError

            # in the runtime we use it to retry the comparison once
            # with the arguments reversed......

            # potentially giving a different implementation of __eq__ on another
            # object a chance to respond
            # If i understood this correctly, this simply means that if other != SortedSet
            # that would return NotImplemented, causing that object to defer to its own __eq__
            # implementation instead of this one
            return NotImplemented
        return self._items == other._items

    def __ne__(self, other):
        if not isinstance(other, SortedSet):
            return NotImplemented
        return self._items != other._items

    # REVERSED PROTOCOL =======

    # note that if __reversed__ is implement
    # python uses that
    # if not, it uses both __getitem__ and __len__
    # instead. Python walks back through the sequence using the two

    # REVERSED PROTOCOL =======

    # VID 11: Index method
    # no need to implement them directly, just inheirt from abc
    # The index method is a mixin when you inherit from it

    # VID 13: Improving the performance of count()
    # from O(N) to O(log n)
    # s.count(i) returns only 0 or 1
    # we also know that the list is always sorted
    # So, we can perform a binary(0 1) search which is faster
    # We don't have to write this from scratch because
    # binary search is implemented in Python

    def count(self, value):
        # from bisect module
        # searches for an item
        # returns the index at which the requested item should
        # be placed in the sequence

        # only works if sorted
        # >> index = bisect_left(self._items, value)

        # then perform two further tests
        # first: returned index w/in the bounds of the collection
        # second: whether there is already the rqd item at that index
        # >> found = (index != len(self._items) and (self._items[index] == value))
        # NOTE to self, shouldn't that be index <= len(self._items)???

        # then convert that bool into int
        # >> return int(found)

        # >> represents the original less efficient code

        # this uses the enchanced __getitem__
        return int(value in self._items)

    # VID 14: notice that:
    # that found represents exactly the same result from __getitem__
    #     found = (index != len(self._items) and (self._items[index] == value))
    # because of that, we replace the code in __contains__ to make it more efficient

    # index() default is also inefficient since
    # it doesn't know that our class is a Sorted Set

    # Vid 14
    def index(self, value, start=0, stop=None):
        index = bisect_left(self._items, value)
        if index != len(self._items) and (self._items[index] == value):
            return index
        raise ValueError('{} not found'.format(repr(value)))

    # Vid 15
    # No need for this because https://docs.python.org/3.4/library/collections.abc.html
    # >>>> def __reversed__(self):
    # note however that even if you remove the inheritance from Sequence,
    # ... it'd still work because of __len__ and __getitem__

    # is there any value in inheriting from Sequence then?
    # yes>
