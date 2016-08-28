class Location:
    """ An object representing an object's grid location.
    Location is defined as a row number and a column number.
    === Attributes ===
    @type location: tuple
        i.e. (row, column)
    """
    def __init__(self, row, column):
        """ Initialize a location.
        @type self: Location
        @type row: int
        @type column: int
        @rtype: None
        """
        # Store in tuple
        self.location = (row, column)

    def __str__(self):
        """ Return a string representation.
        @type self: Location
        @rtype: str
        >>> print(Location(5,6))
        (5,6)
        """
        return "({},{})".format(
            self.location[0], self.location[1])

    def __eq__(self, other):
        """ Return True if self equals other, and false otherwise.
        @type self: Location
        @type other: Location | Any
        @rtype: bool
        >>> first = Location(2,2)
        >>> second = Location(2,2)
        >>> third = Location(4,5)
        >>> first == second
        True
        >>> first == third
        False
        """
        return self.location[0] == other.location[0] and self.location[1] ==\
            other.location[1]


def manhattan_distance(origin, destination):
    """ Return the Manhattan distance between the origin and the destination.
    @type origin: Location
    @type destination: Location
    @rtype: int
    >>> manhattan_distance(Location(2,2), Location(5,6))
    7
    """
    # Take the vertical and horizontal distances and add them together
    return abs(origin.location[0] - destination.location[0]) + abs(
        origin.location[1] - destination.location[1])


def deserialize_location(location_str):
    """ Deserialize a location.
    @type location_str: str
        A location in the format 'row,col'
    @rtype: Location
    >>> serial = "5,6"
    >>> print(deserialize_location(serial))
    (5,6)
    """
    location_list = location_str.split(',')
    return Location(int(location_list[0]), int(location_list[1]))
