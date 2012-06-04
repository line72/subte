#
# Copyright (C) 2012 - Marcus Dillavou
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA.

import os
import weakref

from BaseObject import BaseObject

class Trip(BaseObject):
    '''This is an individual run or a route with
    stops and timetables listed'''

    trips = []
    trip_id = 0

    def __init__(self, name, route, calendar):
        BaseObject.__init__(self)

        self.trip_id = Trip.new_id()
        self.name = name
        self._route = weakref.ref(route)
        self._calendar = weakref.ref(calendar)

        self.stops = {}

        # add us
        Trip.trips.append(self)

    route = property(lambda x: x._route(), None)
    calendar = property(lambda x: x._calendar(), None)

    def get_stop(self, stop):
        if stop not in self.stops:
            self.stops[stop] = TripStop(stop)

        return self.stops[stop]

    def update_stop(self, stop, arrival = None, departure = None):
        if stop is None:
            raise Exception('Invalid Stop')

        trip_stop = self.get_stop(stop)

        if arrival:
            trip_stop.arrival = arrival
        if departure:
            trip_stop.departure = departure

    def write(self, trip_f, stop_times_f):
        self._write(trip_f, '%s,%s,%s,%s,%s,%s,%s\n',
                    self.route.route_id, self.calendar.calendar_id,
                    self.trip_id, '', 0, '', '')

        for i, s in enumerate(self.route.stops):
            trip_stop = self.get_stop(s)
            self._write(stop_times_f, '%s,%s,%s,%s,%s,%s,%s,%s,%s\n',
                        self.trip_id, trip_stop.arrival, trip_stop.departure,
                        trip_stop.stop.stop_id, i+1, '', 0, 0, '')

    @classmethod
    def new_id(cls):
        while True:
            cls.trip_id += 1
            if cls.trip_id not in [x.trip_id for x in Trip.trips]:
                return cls.trip_id

    @classmethod
    def write_trips(cls, directory = '.'):
        f = open(os.path.join(directory, 'trips.txt'), 'w')
        f2 = open(os.path.join(directory, 'stop_times.txt'), 'w')
        # header
        f.write('route_id,service_id,trip_id,trip_headsign,direction_id,block_id,shape_id\n')
        f2.write('trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,pickup_type,drop_off_type,shape_dist_traveled\n')
        for t in cls.trips:
            t.write(f, f2)
        f.close()
        f2.close()

class TripStop(BaseObject):
    def __init__(self, stop, arrival = None, departure = None):
        BaseObject.__init__(self)
        self.arrival = arrival
        self.departure = departure or arrival
        self._stop = weakref.ref(stop)

    stop = property(lambda x: x._stop(), None)
