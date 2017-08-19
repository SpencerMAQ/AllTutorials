class SortedSet:
    """
    Only unique elements but ordered unlike a set
    """
    def __init__(self, items=None):
        self._items = sorted(items) if items is not None else []

    # container protocl "in"
    # without defining the iterable protocol
    # unittest would return four errors

    def __contains__(self, item):
        return item in self._items

    def __len__(self):
        return len(self._items)
