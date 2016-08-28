"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.
=== Constants ===
@type WAITING: str
    A constant used for the waiting rider status.
@type CANCELLED: str
    A constant used for the cancelled rider status.
@type SATISFIED: str
    A constant used for the satisfied rider status
"""

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:
    """ A rider with these attributes:
    @type id: str -- unique identifier for the rider.
    @type origin: Location -- the origin of the rider.
    @type destination: Location -- the Rider's desired destination.
    @type status: str -- the rider's current status.
    @type patience: int -- the number of minutes the driver is willing to wait
                           to be picked up before they cancel their ride.
    """
    def __init__(self, unique_id, _origin, _destination, patience):
        """ Initialize new rider with a unique identifier,
        origin, destination, and status.
        @type self: Rider
        @type unique_id: str
        @type _origin: Location
        @type _destination: Location
        @type patience: int
        @rtype: None
        """
        self.id, self.origin, self.destination, self.status, self.patience = \
            unique_id, _origin, _destination, WAITING, patience
        self.initial = None

    def __lt__(self, other):
        """ Return True iff this Rider is less than <other>.
        @type self: Rider
        @type other: Rider
        @rtype: bool
        >>> first = Rider("Jorge", (1,1), (1,2), 14)
        >>> second = Rider("James", (2,3), (4,4), 5)
        >>> first < second
        False
        >>> second < first
        True
        """
        return self.patience < other.patience

    def __str__(self):
        """ Return a string representation.
        @type self: Rider
        @rtype: str
        >>> a = Rider("Jorge", (1,1), (1,2), 14)
        >>> print(a)
        Jorge
        """
        return self.id
