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
        has_trips = False
        for i, s in enumerate(self.route.stops):
            trip_stop = self.get_stop(s)


            #!mwd - This isn't correct
            #  If we have a '-' that means this stop isn't included
            #   in this trip, so we *should* make a different trip
            #   for it
            # If a stop has a time, add the seconds onto it
            arrival = trip_stop.arrival
            departure = trip_stop.departure

            if trip_stop.arrival == '-':
                # not included in this trip
                continue

            has_trips = True

            if trip_stop.arrival is None or len(trip_stop.arrival) == 0:
                arrival = ''
            elif len(trip_stop.arrival.split(':')) == 2:
                arrival = '%s:00' % trip_stop.arrival

            if trip_stop.departure == '-' or trip_stop.departure is None or len(trip_stop.departure) == 0:
                departure = arrival
            elif len(trip_stop.departure.split(':')) == 2:
                departure = '%s:00' % trip_stop.departure

            self._write(stop_times_f, '%s,%s,%s,%s,%s,%s,%s,%s,%s\n',
                        self.trip_id, arrival, departure,
                        trip_stop.stop.stop_id, i+1, '', 0, 0, '')

        if has_trips:
            shape_id = ''
            if self.route.path is not None:
                shape_id = self.route.path.path_id


            self._write(trip_f, '%s,%s,%s,%s,%s,%s,%s\n',
                        self.route.route_id, self.calendar.calendar_id,
                        self.trip_id, '', 0, '', shape_id)



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
