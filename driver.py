from location import Location, manhattan_distance
from rider import Rider, SATISFIED


class Driver:
    """ A driver for a ride-sharing service.
    === Attributes ===
    @type id: str
        A unique identifier for the driver.
    @type location: Location
        The current location of the driver.
    @type is_idle: bool
        A property that is True if the driver is idle and False otherwise.
    """

    def __init__(self, identifier, location, speed):
        """ Initialize a Driver.
        @type self: Driver
        @type identifier: str
        @type location: Location
        @type speed: int
        @rtype: None
        """
        self.id, self.location, self.speed, self.is_idle = identifier, \
            location, speed, None

    def __str__(self):
        """ Return a string representation.
        @type self: Driver
        @rtype: str
        >>> a = Driver("Tom", Location(5,6), 2)
        >>> print(a)
        Tom
        """
        return self.id

    def __eq__(self, other):
        """ Return True if self equals other, and false otherwise.
        @type self: Driver
        @rtype: bool
        >>> first = Driver("Tom", Location(5,6), 2)
        >>> second = Driver("Tom", Location(2,2), 6)
        >>> third = Driver("Carl", Location(5,6), 2)
        >>> first == second
        False
        >>> first == third
        False
        """
        # Everything must be the same
        return self.id == other.id and self.location == other.location and \
            self.speed == other.speed

    def get_travel_time(self, destination):
        """ Return the time it will take to arrive at the destination,
        rounded to the nearest integer.
        @type self: Driver
        @type destination: Location
        @rtype: int
        >>> a = Driver("Tom", Location(5,6), 2)
        >>> a.get_travel_time(Location(2,2))
        4
        >>> a.get_travel_time(Location(5,4))
        1
        """
        # Time is distance divided by speed
        return round(manhattan_distance(self.location, destination) /
                     self.speed)

    def start_drive(self, location):
        """ Start driving to the location and return the time the drive will take.
        @type self: Driver
        @type location: Location
        @rtype: int
        >>> a = Driver("Tom", Location(5,6), 2)
        >>> a.start_drive(Location(5,4))
        1
        """
        self.is_idle = False
        return self.get_travel_time(location)

    def end_drive(self):
        """ End the drive and arrive at the destination.
        Precondition: self.destination is not None.
        @type self: Driver
        @rtype: None
        """
        self.is_idle = True

    def start_ride(self, rider):
        """ Start a ride and return the time the ride will take.
        @type self: Driver
        @type rider: Rider
        @rtype: int
        >>> a = Driver("Tom", Location(5,6), 2)
        >>> a.start_ride(Rider("Jorge", Location(1, 1), Location(1, 2), 14))
        4
        """
        self.is_idle = False
        # Change the rider status
        rider.status = SATISFIED
        return self.get_travel_time(rider.destination)

    def end_ride(self):
        """ End the current ride, and arrive at the rider's destination.
        Precondition: The driver has a rider.
        Precondition: self.destination is not None.
        @type self: Driver
        @rtype: None
        """
        self.is_idle = True
        # rider status is not changed
