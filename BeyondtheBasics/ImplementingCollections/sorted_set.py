class SortedSet:

    def __init__(self, items=None):
        self._items = sorted(items) if items is not None else []

    # container protocl "in"
    # without defining the iterable protocol
    # unittest would return four errors

    def __contains__(self, item):
        return item in self._items
