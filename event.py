"""Simulation Events
This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from rider import Rider, WAITING, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import deserialize_location
from monitor import Monitor, RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF


class Event:
    """ An event.
    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.
    This class is abstract; subclasses must implement do().
    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.
    Document any such changes carefully!
    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    """

    def __init__(self, timestamp):
        """ Initialize an Event with a given timestamp.
        @type self: Event
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @rtype: None
        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other):
        """ Return True iff this Event is equal to <other>.
        Two events are equal iff they have the same timestamp.
        @type self: Event
        @type other: Event
        @rtype: bool
        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other):
        """ Return True iff this Event is not equal to <other>.
        @type self: Event
        @type other: Event
        @rtype: bool
        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other):
        """ Return True iff this Event is less than <other>.
        @type self: Event
        @type other: Event
        @rtype: bool
        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other):
        """ Return True iff this Event is less than or equal to <other>.
        @type self: Event
        @type other: Event
        @rtype: bool
        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other):
        """ Return True iff this Event is greater than <other>.
        @type self: Event
        @type other: Event
        @rtype: bool
        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other

    def __ge__(self, other):
        """ Return True iff this Event is greater than or equal to <other>.
        @type self: Event
        @type other: Event
        @rtype: bool
        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other

    def __str__(self):
        """ Return a string representation of this event.
        @type self: Event
        @rtype: str
        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher, monitor):
        """ Do this Event.
        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.
        Notify the monitor of any activities that have occurred during the
        event.
        Return a list of new events spawned by this event (making sure the
        timestamps are correct).
        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        @type self: Event
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """ A rider requests a driver.
    === Attributes ===
    @type rider: Rider
        The rider.
    """

    def __init__(self, timestamp, rider):
        """ Initialize a RiderRequest event.
        @type self: RiderRequest
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """ Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.
        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.
        @type self: RiderRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        # Docstring examples have been omitted since a memory address
        # location is returned.
        self.rider.initial = self.timestamp
        # Notify the monitor
        monitor.notify(self.timestamp, RIDER, REQUEST,
                       self.rider.id, self.rider.origin)
        # Begin keeping track of the consequences of the current event
        events = []
        driver = dispatcher.request_driver(self.rider)
        if driver is not None:
            travel_time = driver.start_drive(self.rider.origin)
            events.append(Pickup(self.timestamp + travel_time, self.rider,
                                 driver))
        events.append(Cancellation(self.timestamp + self.rider.patience,
                                   self.rider))
        return events

    def __str__(self):
        """ Return a string representation of this event.
        @type self: RiderRequest
        @rtype: str
        >>> a = RiderRequest(4, Rider("Jorge", (1,1), (1,2), 14))
        >>> print(a)
        4 -- Jorge: Request a driver
        """
        return "{} -- {}: Request a driver".format(self.timestamp, self.rider)


class DriverRequest(Event):
    """ A driver requests a rider.
    === Attributes ===
    @type driver: Driver
        The driver.
    """

    def __init__(self, timestamp, driver):
        """ Initialize a DriverRequest event.
        @type self: DriverRequest
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher, monitor):
        """ Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.
        If a rider is available, return a Pickup event.
        @type self: DriverRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        # Docstring examples have been omitted since a memory address
        # location is returned.
        
        # Notify the monitor about the request.
        monitor.notify(self.timestamp, DRIVER, REQUEST,
                       self.driver.id, self.driver.location)
                       
        # Request a rider from the dispatcher.
        # If there is one available, the driver starts driving towards the
        # rider, and the method returns a Pickup event for when the driver
        # arrives at the riders location.
        events = []
        rider = dispatcher.request_rider(self.driver)
        if rider is not None:
            travel_time = self.driver.start_drive(rider.origin)
            events.append(Pickup(self.timestamp + travel_time, rider,
                                 self.driver))
        return events

    def __str__(self):
        """ Return a string representation of this event.
        @type self: DriverRequest
        @rtype: str
        >>> a = DriverRequest(4, Driver("Tom", (5,6), 2))
        >>> print(a)
        4 -- Tom: Request a rider
        """
        return "{} -- {}: Request a rider".format(self.timestamp, self.driver)


class Cancellation(Event):
    """ A rider cancels a request
    === Attributes ===
    @type rider: Rider
        The rider
    """

    def __init__(self, timestamp, rider):
        """ Initialize a Cancellation event
        @type self: Cancellation
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """ Cancels the request from a waiting rider
        @type self: Cancellation
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: None
        """
        # Notify the monitor
        monitor.notify(self.timestamp, RIDER, CANCEL, self.rider.id,
                       self.rider.origin)
        # Change the rider status
        if self.rider.status is WAITING:
            self.rider.status = CANCELLED
            dispatcher.cancel_ride(self.rider)

    def __str__(self):
        """ Return a string representation of this event.
        @type self: Cancellation
        @rtype: str
        >>> a = Cancellation(4, Rider("Jorge", (1,1), (1,2), 14))
        >>> print(a)
        4 -- Jorge: Cancel request
        """
        return "{} -- {}: Cancel request".format(self.timestamp, self.rider)


class Pickup(Event):
    """ A driver picks up a rider
    === Attributes ===
    @type rider: Rider
        The rider
    @type driver: Driver
        The driver
    """

    def __init__(self, timestamp, rider, driver):
        """ Initialize a Pickup event
        @type self: Pickup
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider
        self.driver = driver

    def do(self, dispatcher, monitor):
        """ Driver picks up a rider
        @type self: Pickup
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        # Docstring examples have been omitted since a memory address
        # location is returned.
        
        # Begin keeping track of the consequences of this event
        events = []
        self.driver.location = self.rider.origin
        if self.rider.initial + self.rider.patience > self.timestamp:
            monitor.notify(self.timestamp, DRIVER, PICKUP, self.driver.id,
                           self.driver.location)
            monitor.notify(self.timestamp, RIDER, PICKUP, self.rider.id,
                           self.rider.origin)

            travel_time = self.driver.start_ride(self.rider)
            # This might change after Dropoff is implemented
            events.append(Dropoff(self.timestamp + travel_time, self.rider,
                                  self.driver))
        else:
            self.driver.end_ride()
            events.append(Cancellation(self.timestamp, self.rider))
            events.append(DriverRequest(self.timestamp, self.driver))
        return events

    def __str__(self):
        """ Return a string representation of this event.
        @type self: Pickup
        @rtype: str
        >>> a = Pickup(4, Rider("Jorge", (1,1), (1,2), 14),\
         Driver("Tom", (5,6), 2))
        >>> print(a)
        4 -- Tom: Pickup Jorge
        """
        return "{} -- {}: Pickup {}".format(self.timestamp, self.driver,
                                            self.rider)


class Dropoff(Event):
    """ A driver drops off a rider
    === Attributes ===
    @type rider: Rider
        The rider
    @type driver: Driver
        The driver
    """

    def __init__(self, timestamp, rider, driver):
        """ Initialize a Dropoff event
        @type self:  Dropoff
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider
        self.driver = driver

    def do(self, dispatcher, monitor):
        """ Driver drops off a rider
        @type self: Dropoff
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: None
        """
        self.driver.location = self.rider.destination
        # Notify the monitor
        monitor.notify(self.timestamp, DRIVER, DROPOFF, self.driver.id,
                       self.rider.destination)
        # Begin keeping track of the consequences of this event
        events = []
        self.driver.end_ride()
        self.rider.status = SATISFIED
        dispatcher.rider_list.remove_particular(self.rider)
        events.append(DriverRequest(self.timestamp, self.driver))
        return events

    def __str__(self):
        """ Return a string representation of this event.
        @type self: Dropoff
        @rtype: str
        >>> a = Dropoff(4, Rider("Jorge", (1,1), (1,2),\
         14), Driver("Tom", (5,6), 2))
        >>> print(a)
        4 -- Tom: Drop off Jorge
        """
        return "{} -- {}: Drop off {}".format(self.timestamp, self.driver,
                                              self.rider)


def create_event_list(filename):
    """ Return a list of Events based on raw list of events in <filename>.
    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.
    @type filename: str
        The name of a file that contains the list of events.
    @rtype: list[Event]
    """
    # Docstring examples have been omitted since a memory address
    # location is returned/requires user input <filename>
    
    events = []
    # Open the file
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                # Skip lines that are blank or start with #.
                continue

            # Create a list of words in the line, e.g.
            # ['10', 'RiderRequest', 'Cerise', '4,2', '1,5', '15'].
            # Note that these are strings, and you'll need to convert some
            # of them to a different type.
            tokens = line.split()
            timestamp = int(tokens[0])
            event_type = tokens[1]
            event = None
            # HINT: Use Location.deserialize to convert the location string to
            # a location.
            if event_type == "RiderRequest":
                actor_id = tokens[2]
                origin = deserialize_location(tokens[3])
                destination = deserialize_location(tokens[4])
                patience = int(tokens[5])
                event = RiderRequest(timestamp, Rider(actor_id, origin,
                                                      destination, patience))
            elif event_type == "DriverRequest":
                actor_id = tokens[2]
                location = deserialize_location(tokens[3])
                speed = int(tokens[4])
                event = DriverRequest(timestamp, Driver(actor_id, location,
                                                        speed))
            events.append(event)
    return events
