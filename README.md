# ride-sharing-simulation

# overview
Car testers use crash-test dummies because the danger of human carnage is too great to use living subjects.
Climatologists build computer models of changing meteorological patterns because they can't afford the
decades or centuries to wait observing the actual patterns. Weapons manufacturers test models of their
products on computers so that they can safely enjoy their profits far away from the horrors those products
produce.

Computer simulations are great for exploring "what if" questions about scenarios before, or instead of,
letting those scenarios play out in the real world. We hope this is a safer and faster approach than
having taxis, Uber, riders, and municipal politicians live through the scenarios on the streets.

# simulation overview
The simulation consists of four key entities: Riders, drivers, the dispatcher, and the monitor. Riders request
rides from their current location to a destination. Drivers drive to pickup and drop off riders. The dispatcher
receives and satises requests from drivers for a rider, and from riders for a driver. The monitor keeps track
of activities in the simulation, and when asked, generates a report of what happened during the simulation.
The simulation plays out on a simplied city grid, where the location of riders and drivers is the intersection they are closest to. An intersection is represented by a pair of positive integers: The number of a north/south street, and the number of an east/west street. For example 1,2 is the intersection of Street 1
north/south with Street 2 east/west.

When a rider requests a driver, the dispatcher tries to assign a driver to the rider. If there is no driver
available, the dispatcher keeps track of the rider request, waiting for a driver to become available. A rider
will cancel their request if they have to wait too long for a pick up.
When a driver requests a rider, the dispatcher assigns a waiting rider, if any. If this is the driver's first
request, the dispatcher registers the driver in its fleet. Once registered, a driver never unregisters. This simulation is simplified in many ways.

And so it goes. There is clearly a connection between how long riders are waiting to be picked up and
how many drivers are available and waiting to be assigned riders. The simulation can measure how this
connection affects rider waiting times and driver earnings. It will to monitor all appropriate events:
riders requesting rides, being picked up (or possibly cancelling first), then being dropped off; and drivers
requesting to be assigned riders
