class Container:
    """ A container that holds objects.
    This is an abstract class.  Only child classes should be instantiated.
    """

    def add(self, item):
        """ Add <item> to this Container.
        @type self: Container
        @type item: Object
        @rtype: None
        """
        raise NotImplementedError("Implemented in a subclass")

    def remove(self):
        """ Remove and return a single item from this Container.
        @type self: Container
        @rtype: Object
        """
        raise NotImplementedError("Implemented in a subclass")

    def is_empty(self):
        """ Return True iff this Container is empty.
        @type self: Container
        @rtype: bool
        """
        raise NotImplementedError("Implemented in a subclass")


class PriorityQueue(Container):
    """ A queue of items that operates in priority order.

    Items are removed from the queue according to priority; the item with the
    highest priority is removed first. Ties are resolved in FIFO order,
    meaning the item which was inserted *earlier* is the first one to be
    removed.

    Priority is defined by the rich comparison methods for the objects in the
    container (__lt__, __le__, __gt__, __ge__).

    If x < y, then x has a *HIGHER* priority than y.

    All objects in the container must be of the same type.
     === Private Attributes ===
     @type _items: list
         The items stored in the priority queue.
     === Representation Invariants ===
     _items is a sorted list, where the first item in the queue is the
     item with the highest priority.
     """

    def __init__(self):
        """ Initialize an empty PriorityQueue.
        @type self: PriorityQueue
        @rtype: None
        """
        self._items = []

    def __str__(self):
        """ Return a user-friendly str representation of PriorityQueue <self>
        @type self: PriorityQueue
        @rtype: str
        >>> a = PriorityQueue()
        >>> a.add(8)
        >>> a.add(9)
        >>> a.add(2)
        >>> print(a)
        [2, 8, 9]
        """
        # Start a string ret that will have all
        # necessary components appended to it
        ret = "["
        # As long as there is another element in self._items,
        # append its string representation to ret
        for i in range(len(self._items)):
            ret = ret + str(self._items[i]) + ", "
        # Finishing touch on ret to close the brackets
        ret = ret[0:len(ret)-2] + "]"
        # If self._items was empty, modify ret
        if ret == "]":
            ret = "None"
        return ret

    def contains(self, item):
        """ Return if PriorityQueue <self> contains <item>
        @type self: PriorityQueue
        @type item: Object
        @rtype: bool
        >>> a = PriorityQueue()
        >>> a.add(7)
        >>> a.contains(4)
        False
        >>> a.contains(7)
        True
        """
        return item in self._items

    def first_element(self):
        """ Return the first element in the PriorityQueue <self>
        @type self: PriorityQueue
        @rtype: object
        >>> a = PriorityQueue()
        >>> a.add(9)
        >>> a.first_element()
        9
        >>> a.add(2)
        >>> a.first_element()
        2
        """
        return self._items[0]

    def remove_particular(self, particular):
        """ Return particular element from PriorityQueue <self>
        @type self: PriorityQueue
        @type particular: Object
        @rtype: None
        """
        counter = 0
        while counter < len(self._items):
            if self._items[counter] == particular:
                self._items.pop(counter)
            counter += 1

    def remove(self):
        """ Remove and return the next item from this PriorityQueue.
        Precondition: <self> should not be empty.
        @type self: PriorityQueue
        @rtype: object
        >>> pq = PriorityQueue()
        >>> pq.add("red")
        >>> pq.add("blue")
        >>> pq.add("yellow")
        >>> pq.add("green")
        >>> pq.remove()
        'blue'
        >>> pq.remove()
        'green'
        >>> pq.remove()
        'red'
        >>> pq.remove()
        'yellow'
        """
        return self._items.pop(0)

    def is_empty(self):
        """ Return true iff this PriorityQueue is empty.
        @type self: PriorityQueue
        @rtype: bool
        >>> pq = PriorityQueue()
        >>> pq.is_empty()
        True
        >>> pq.add("thing")
        >>> pq.is_empty()
        False
        """
        return len(self._items) == 0

    def __len__(self):
        """ Return length of <self>
        @type self: PriorityQueue
        @rtype: int
        >>> pg = PriorityQueue()
        >>> pg.add(5)
        >>> pg.add(3)
        >>> len(pg)
        2
        >>> pg.add(1)
        >>> len(pg)
        3
        """
        return len(self._items)

    def add(self, item):
        """ Add <item> to this PriorityQueue.
        @type self: PriorityQueue
        @type item: object
        @rtype: None
        >>> pq = PriorityQueue()
        >>> pq.add("yellow")
        >>> pq.add("blue")
        >>> pq.add("red")
        >>> pq.add("green")
        >>> pq._items
        ['blue', 'green', 'red', 'yellow']
        """
        flag = True
        # If item is the only element, it can be appended
        if len(self._items) == 0:
            self._items.append(item)
        else:
            i = 0
            # Determine the correct position for item and add it
            for i in range(len(self._items) - 1, -1, -1):
                if item < self._items[i]:
                    pass
                elif flag:
                    self._items = self._items[:i + 1] + [item] + self._items[
                                                                 i + 1:]
                    flag = False
            if flag:
                self._items = self._items[:i] + [item] + self._items[i:]

    @property
    def items(self):
        """ Return self._items
        @type self: PriorityQueue
        @rtype: list
        >>> ls = PriorityQueue()
        >>> ls.add(3)
        >>> ls.add(8)
        >>> ls.items
        [3, 8]
        >>> ls.add(1)
        >>> ls.items
        [1, 3, 8]
        """
        return self._items
        
if __name__ == '__main__':
    import doctest
    doctest.mod()
