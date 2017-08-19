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
        return self._items[item]