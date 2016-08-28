from container import PriorityQueue
from dispatcher import Dispatcher
from event import create_event_list
from monitor import Monitor


class Simulation:
    """ A simulation.
    This is the class which is responsible for setting up and running a
    simulation.
    The API is given to you: your main task is to implement the two methods
    according to their docstrings.
    Of course, you may add whatever private attributes and methods you want.
    But because you should not change the interface, you may not add any public
    attributes or methods.
    This is the entry point into your program, and in particular is used for
    auto-testing purposes. This makes it ESSENTIAL that you do not change the
    interface in any way!
    === Private Attributes ===
    @type _events: PriorityQueue[Event]
        A sequence of events arranged in priority determined by the event
        sorting order.
    @type _dispatcher: Dispatcher
        The dispatcher associated with the simulation.
    """

    def __init__(self):
        """ Initialize a Simulation.
        @type self: Simulation
        @rtype: None
        """
        self._events = PriorityQueue()
        self._dispatcher = Dispatcher()
        self._monitor = Monitor()

    def run(self, initial_events):
        """ Run the simulation on the list of events in <initial_events>.
        Return a dictionary containing statistics of the simulation,
        according to the specifications in the assignment handout.
        @type self: Simulation
        @type initial_events: list[Event]
            An initial list of events.
        @rtype: dict[str, object]
        >>> a = Simulation()
        >>> a.run(create_event_list("events_small.txt"))
        1 -- Dan: Request a driver
        10 -- Arnold: Request a rider
        12 -- Arnold: Pickup Dan
        16 -- Dan: Cancel request
        17 -- Arnold: Drop off Dan
        17 -- Arnold: Request a rider
        {'driver_total_distance': 14.0, 'rider_wait_time': \
11.0, 'driver_ride_distance': 10.0}
        """
        # Load all the initial events
        for event in initial_events:
            self._events.add(event)
        # Continue running until there are no more events in the queue
        while not self._events.is_empty():
            curr_event = self._events.remove()
            new_event = curr_event.do(self._dispatcher, self._monitor)
            if new_event is not None and new_event != []:
                for i in new_event:
                    self._events.add(i)
            print(curr_event)
        return self._monitor.report()


if __name__ == "__main__":
    events = create_event_list("events_small.txt")
    sim = Simulation()
    final_stats = sim.run(events)
    print(final_stats)
