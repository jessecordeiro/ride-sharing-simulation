from driver import Driver
from rider import Rider
from container import PriorityQueue


class Dispatcher:
    """ A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.
    === Attributes ===
    @type driver_list: PriorityQueue
        A prioritized record of all registered drivers
    @type rider_list: PriorityQueue
        A prioritized record of all registered riders
    """

    def __init__(self):
        """ Initialize a Dispatcher.
        @type self: Dispatcher
        @rtype: None
        """
        self.driver_list = PriorityQueue()
        self.rider_list = PriorityQueue()

    def __str__(self):
        """ Return a string representation.
        @type self: Dispatcher
        @rtype: str
        >>> a = Dispatcher()
        >>> a.request_driver(Rider("Jorge", (1, 1), (1, 2), 14))
        >>> a.request_driver(Rider("James", (2,3), (4,4), 5))
        >>> print(a)
        List of available drivers: None
        List of available riders: [James, Jorge]
        """
        return "List of available drivers: {}\nList of available" \
               " riders: {}".format(self.driver_list, self.rider_list)

    def request_driver(self, rider):
        """ Return a driver for the rider, or None if no driver is available.
        Add the rider to the waiting list if there is no available driver.
        @type self: Dispatcher
        @type rider: Rider
        @rtype: Driver | None
        """
        # Docstring examples have been omitted since a memory address
        # location is returned.
        if self.driver_list.is_empty():
            if not self.rider_list.contains(rider):
                self.rider_list.add(rider)
            return None
        else:
            # Find the driver who can pick up rider the fastest
            i = 0
            driver = self.driver_list.first_element()
            curr_time = driver.get_travel_time(rider.origin)
            while i < len(self.driver_list):
                if self.driver_list.items[i].get_travel_time(rider.origin) \
                        < curr_time:
                    driver = self.driver_list.items[i]
                    curr_time = driver.get_travel_time(rider.origin)
                i += 1
            return driver

    def request_rider(self, driver):
        """ Return a rider for the driver, or None if no rider is available.
        If this is a new driver, register the driver for future rider requests.
        @type self: Dispatcher
        @type driver: Driver
        @rtype: Rider | None
        """
        # Docstring examples have been omitted since a memory address
        # location is returned.
        if not self.driver_list.contains(driver):
            self.driver_list.items.append(driver)
        if not self.rider_list.is_empty():
            return self.rider_list.first_element()
        return None

    def cancel_ride(self, rider):
        """ Cancel the ride for rider.
        @type self: Dispatcher
        @type rider: Rider
        @rtype: None
        """
        self.rider_list.remove_particular(rider)
