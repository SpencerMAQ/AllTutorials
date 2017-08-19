class SortedSet:
    """
    Only unique elements but ordered unlike a set
    """
    def __init__(self, items=None):
        self._items = sorted(set(items)) if items is not None else []

    # container protocl "in"
    # without defining the iterable protocol
    # unittest would return four errors

    def __contains__(self, item):
        return item in self._items

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