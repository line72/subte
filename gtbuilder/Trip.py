import weakref

from BaseObject import BaseObject

class Trip(BaseObject):
    '''This is an individual run or a route with
    stops and timetables listed'''

    trips = []

    def __init__(self, name, route, calendar):
        BaseObject.__init__(self)

        self.name = name
        self.route = route
        self.calendar = calendar

        self.stops = []

        # add us
        Trip.trips.append(weakref.ref(self))

    def add_stop(self, stop, arrival, depature = None):
        if stop is None:
            raise Exception('Invalid Stop')
        self.stops.append(TripStop(stop, arrival, depature))

    def write(self, trip_f, stop_times_f):
        self._write(trip_f, '%s,%s,%s,%s,%s,%s,%s\n',
                    self.route.route_id, self.calendar.service_id,
                    self.name, '', 0, '', '')

        for i, s in enumerate(self.stops):
            self._write(stop_times_f, '%s,%s,%s,%s,%s,%s,%s,%s,%s\n',
                        self.name, s.arrival, s.departure,
                        s.stop.stop_id, i+1, '', 0, 0, '')

    @classmethod
    def write_trips(cls):
        f = open('trips.txt', 'w')
        f2 = open('stop_times.txt', 'w')
        # header
        f.write('route_id,service_id,trip_id,trip_headsign,direction_id,block_id,shape_id\n')
        f2.write('trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,pickup_type,drop_off_type,shape_dist_traveled\n')
        for t in cls.trips:
            if t():
                t().write(f, f2)
        f.close()
        f2.close()

class TripStop(BaseObject):
    def __init__(self, stop, arrival, departure = None):
        self.arrival = arrival
        self.departure = departure or arrival
        self.stop = stop
