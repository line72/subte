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

    def __init__(self, name, trip_route, calendar):
        BaseObject.__init__(self)

        self.trip_id = Trip.new_id()
        self.name = name
        self._trip_route = weakref.ref(trip_route)
        self._calendar = weakref.ref(calendar)

        self.stops = []

        self._next_block = None
        self._previous_block = None

        # add us
        Trip.trips.append(self)

    trip_route = property(lambda x: x._trip_route(), None)
    calendar = property(lambda x: x._calendar(), None)
    first_block = property(lambda x: x.get_first_block(), None)
    next_block = property(lambda x: x.get_next_block(), lambda x, v: x.set_next_block(v))
    previous_block = property(lambda x: x.get_previous_block(), lambda x, v: x.set_previous_block(v))

    def destroy(self):
        self.stops = []

        try:
            Trip.trips.remove(self)
        except ValueError, e:
            pass

    def add_trip_stop(self, tripstop):
        self.stops.append(tripstop)

    def insert_stop_at(self, index, stop):
        self.stops.insert(index, stop)

    def remove_trip_stop(self, tripstop):
        try: self.stops.remove(tripstop)
        except ValueError, e: pass

    def remove_trip_stop_at(self, index):
        try: self.stops.pop(index)
        except ValueError, e: pass

    def increment_trip_stop_at(self, index):
        if index == 0:
            return False

        try:
            tripstop = self.stops.pop(index)
            self.stops.insert(index-1, tripstop)
        except ValueError, e: 
            return False

        return True

    def decrement_trip_stop_at(self, index):
        if index == len(self.stops) - 1:
            return False

        try:
            tripstop = self.stops.pop(index)
            self.stops.insert(index+1, tripstop)
        except ValueError, e: 
            return False

        return True

    def get_stop(self, stop):
        ts = None
        for tripstop in self.stops:
            if tripstop.stop == stop:
                ts = tripstop
                break

        if ts is None:
            ts = TripStop(stop)
            self.stops.append(ts)

        return ts

    def update_stop(self, stop, arrival = None, departure = None):
        if stop is None:
            raise Exception('Invalid Stop')

        trip_stop = self.get_stop(stop)

        if arrival:
            trip_stop.arrival = arrival
        if departure:
            trip_stop.departure = departure

    def has_blocks(self):
        '''Check to see if we are linked to 
        any other trips through blocks'''
        return (self.previous_block != None or self.next_block != None)

    def get_next_block(self):
        if self._next_block:
            return self._next_block()
        return self._next_block

    def set_next_block(self, b, link = True):
        if link:
            if self.next_block:
                self.next_block.set_previous_block(None, False)

        if b:
            self._next_block = weakref.ref(b)
            if link:
                b.set_previous_block(self, False)
        else:
            self._next_block = None


    def get_previous_block(self):
        if self._previous_block:
            return self._previous_block()
        return self._previous_block

    def set_previous_block(self, b, link = True):
        if link:
            if self.previous_block:
                self.previous_block.set_next_block(None, False)

        if b:
            self._previous_block = weakref.ref(b)
            if link:
                b.set_next_block(self, False)
        else:
            self._previous_block = None

    def get_first_block(self):
        '''Return the first block (which may be us)
        Return None if we are not linked to any other
        trips through blocks'''
        if not self.has_blocks():
            return None

        t = self.previous_block
        prev = t

        while t != None:
            prev = t
            t = t.previous_block

        if prev is None:
            return self

        return prev

    def get_block_id(self):
        '''Return the block id(str) or None if
        we aren't linked to any other trips
        through blocks'''

        if not self.has_blocks():
            return None

        return 'B_%s' % (self.get_first_block().trip_id)


    def write(self, trip_f, stop_times_f):
        has_trips = False
        for i, s in enumerate(self.stops):
            trip_stop = s


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
            if self.trip_route.path is not None:
                shape_id = self.trip_route.path.path_id

            block_id = self.get_block_id()

            self._write(trip_f, '%s,%s,%s,%s,%s,%s,%s\n',
                        self.trip_route.route.route_id, self.calendar.calendar_id,
                        self.trip_id, self.trip_route.headsign, self.trip_route.direction, block_id, shape_id)


    @classmethod
    def get(cls, trip_id):
        for trip in cls.trips:
            if trip.trip_id == trip_id:
                return trip
        return None

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
