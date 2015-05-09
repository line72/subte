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

import os, sys
import weakref
import csv

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
    calendar = property(lambda x: x.get_calendar(), lambda x, c: x.set_calendar(c))
    first_block = property(lambda x: x.get_first_block(), None)
    next_block = property(lambda x: x.get_next_block(), lambda x, v: x.set_next_block(v))
    previous_block = property(lambda x: x.get_previous_block(), lambda x, v: x.set_previous_block(v))

    def destroy(self):
        self.stops = []

        try:
            Trip.trips.remove(self)
        except ValueError, e:
            pass

    def get_calendar(self):
        try: return self._calendar()
        except Exception, e: return None

    def set_calendar(self, calendar):
        if calendar == None:
            self._calendar = None
        else:
            self._calendar = weakref.ref(calendar)

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

    def get_id(self):
        if self.gtfs_id:
            return self.gtfs_id
        return self.trip_id

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
                        self.get_id(), arrival, departure,
                        trip_stop.stop.get_id(), i+1, '', 0, 0, '')

        if has_trips:
            shape_id = ''
            if self.trip_route.path is not None:
                shape_id = self.trip_route.path.get_id()

            block_id = self.get_block_id()

            self._write(trip_f, '%s,%s,%s,%s,%s,%s,%s\n',
                        self.trip_route.route.get_id(), self.calendar.get_id(),
                        self.get_id(), self.trip_route.headsign, self.trip_route.direction, block_id, shape_id)


    @classmethod
    def clear(cls):
        for trip in cls.trips:
            trip.destroy()

        cls.trips = []
        cls.trip_id = 0

    @classmethod
    def get(cls, trip_id):
        for trip in cls.trips:
            if trip.trip_id == trip_id:
                return trip
        return None

    @classmethod
    def get_by_gtfs_id(cls, gtfs_id):
        for trip in cls.trips:
            if trip.gtfs_id == gtfs_id:
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

    @classmethod
    def import_trips(cls, directory):
        from Route import Route
        from Calendar import Calendar
        from TripRoute import TripRoute
        from Path import Path
        from Stop import Stop

        try:
            f = open(os.path.join(directory, 'trips.txt'), 'rb')
            reader = csv.reader(f)

            mappings = {'route_id': ('route', lambda x: Route.get_by_gtfs_id(x)),
                        'service_id': ('calendar', lambda x: Calendar.get_by_gtfs_id(x)),
                        'trip_id': ('name', lambda x: x),
                        'trip_headsign': ('headsign', lambda x: x),
                        'direction_id': ('direction', lambda x: int(x) if x else 0),
                        'shape_id': ('path', lambda x: Path.get_by_gtfs_id(x)),
            }

            # create a headers with an index
            headers = reader.next()
            r_headers = dict([(x, i) for i, x in enumerate(headers)])

            for l2 in reader:
                if len(l2) != len(headers):
                    print >> sys.stderr, 'Invalid line', l2, headers
                    continue
                
                kw = {}
                for i, a in enumerate(l2):
                    key = headers[i]
                    if key in mappings:
                        kw[mappings[key][0]] = mappings[key][1](BaseObject.unquote(a))
                # create the trip route
                trip_route = TripRoute(**kw)
                # set the id
                trip_route.gtfs_id = BaseObject.unquote(l2[r_headers['trip_id']])
                # create a trip
                trip = trip_route.add_trip()
                trip.gtfs_id = BaseObject.unquote(l2[r_headers['trip_id']])

            # go through the list again and set block ids
            #!mwd - I'm not sure how to do this. We link
            #  blocks by trip ids, but block ids are 
            #  random in gtfs, so we have no way to link
            #  them back

        except IOError, e:
            print >> sys.stderr, 'Unable to open trips.txt:', e

        # load all the stops
        try:
            f = open(os.path.join(directory, 'stop_times.txt'), 'rb')
            reader = csv.reader(f)

            mappings = {'arrival_time': ('arrival', lambda x: x),
                        'departure_time': ('departure', lambda x: x),
                        'stop_id': ('stop', lambda x: Stop.get_by_gtfs_id(x)),
            }

            # create a headers with an index
            headers = reader.next()
            r_headers = dict([(x, i) for i, x in enumerate(headers)])

            for l2 in reader:
                if len(l2) != len(headers):
                    print >> sys.stderr, 'Invalid line', l2, headers
                    continue
                
                kw = {}
                for i, a in enumerate(l2):
                    key = headers[i]
                    if key in mappings:
                        kw[mappings[key][0]] = mappings[key][1](BaseObject.unquote(a))

                # find the corresponding trip
                trip_id = BaseObject.unquote(l2[r_headers['trip_id']])
                trip = Trip.get_by_gtfs_id(trip_id)
                if trip is None:
                    print >> sys.stderr, 'no trip for id', trip_id

                # add the trip stop
                stop_id = BaseObject.unquote(l2[r_headers['stop_id']])
                stop = Stop.get_by_gtfs_id(stop_id)
                trip.trip_route.add_stop(stop)

                trip_stop = trip.stops[-1]
                trip_stop.arrival = BaseObject.unquote(l2[r_headers['arrival_time']])
                trip_stop.departure = BaseObject.unquote(l2[r_headers['departure_time']])

        except IOError, e:
            print >> sys.stderr, 'Unable to open stop_times.txt:', e
        

        # merge trip routes
        TripRoute.merge()


class TripStop(BaseObject):
    def __init__(self, stop, arrival = None, departure = None):
        BaseObject.__init__(self)
        self.arrival = arrival
        self.departure = departure or arrival
        self._stop = weakref.ref(stop)

    stop = property(lambda x: x._stop(), None)
