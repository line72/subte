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
from Trip import Trip, TripStop
from Frequency import Frequency

class TripRoute(BaseObject):
    '''This is a group of trips that
    all share the same stops along a route'''

    trip_routes = []
    trip_route_id = 0

    def __init__(self, name, route, calendar, headsign, direction, path = None):
        BaseObject.__init__(self)

        self.trip_route_id = TripRoute.new_id()
        self.name = name
        self._route = None
        self._calendar = None

        self.set_route(route)
        self.set_calendar(calendar)

        self.headsign = headsign
        self.direction = direction
        self.path = path

        self.wheelchair_accessible = 0

        self.trips = []
        self.frequencies = []

        self._stops = []

        # add us
        TripRoute.trip_routes.append(self)

    route = property(lambda x: x.get_route(), lambda x, r: x.set_route(r))
    calendar = property(lambda x: x.get_calendar(), lambda x, c: x.set_calendar(c))
    stops = property(lambda x: x._stops[:], None)

    def destroy(self):
        for trip in self.trips:
            trip.destroy()
        self.trips = []
        self._stops = []

        try:
            TripRoute.trip_routes.remove(self)
        except ValueError, e:
            pass

    def copy(self):
        '''Make a shallow copy.
        This doesn't copy trips or frequencies'''
        tr = TripRoute(self.name + ' Copy', self.route, self.calendar, self.headsign, self.direction, self.path)
        for s in self._stops:
            tr.add_stop(s)

        return tr

    def add_trip(self):
        trip = Trip('', self, self.calendar)

        # add the stops
        for stop in self._stops:
            trip.add_trip_stop(TripStop(stop))

        self.trips.append(trip)

        return trip

    def remove_trip(self, trip):
        try: self.trips.remove(trip)
        except ValueError, e: pass

    def add_frequency(self, start, end, headway):
        frequency = Frequency(self, start, end, headway)

        self.frequencies.append(frequency)

        return frequency

    def remove_frequency(self, frequency):
        try: self.frequencies.remove(frequency)
        except ValueError, e: pass

    def clear_stops(self):
        self._stops = []
        for trip in self.trips:
            trip.stops = []

    def add_stop(self, stop):
        self._stops.append(stop)

        # for all our trips
        for trip in self.trips:
            t = TripStop(stop)
            trip.add_trip_stop(t)

    def insert_stop_at(self, index, stop):
        self._stops.insert(index, stop)

        for trip in self.trips:
            trip.insert_top_at(index, stop)

    def remove_stop(self, stop):
        '''Remove any references to a stop 
        since it isn't part of the route anymore.'''
        try:
            while True:
                index = self._stops.index(stop)
                self.remove_stop_at(index)
        except ValueError, e:
            return True

    def remove_stop_at(self, index):
        try: self._stops.pop(index)
        except ValueError, e: pass

        # for all our trip
        for trip in self.trips:
            trip.remove_trip_stop_at(index)

    def increment_stop_at(self, index):
        if index == 0:
            return False

        try:
            s = self._stops.pop(index)
            self._stops.insert(index-1, s)
        except ValueError, e: 
            return False

        for trip in self.trips:
            trip.increment_trip_stop_at(index)

    def decrement_stop_at(self, index):
        if index == len(self.stops) - 1:
            return False

        try:
            s = self._stops.pop(index)
            self._stops.insert(index+1, s)
        except ValueError, e: 
            return False

        for trip in self.trips:
            trip.decrement_trip_stop_at(index)

    def set_calendar(self, calendar):
        if calendar == None:
            self._calendar = None
        else:
            self._calendar = weakref.ref(calendar)

    def get_calendar(self):
        try: return self._calendar()
        except Exception, e: return None

    def set_route(self, route):
        if route == None:
            self._route = None
        else:
            self._route = weakref.ref(route)

    def get_route(self):
        try: return self._route()
        except Exception, e: return None

    @classmethod
    def get(cls, trip_route_id):
        for trip_route in cls.trip_routes:
            if trip_route.trip_route_id == trip_route_id:
                return trip_route
        return None

    @classmethod
    def new_id(cls):
        while True:
            cls.trip_route_id += 1
            if cls.trip_route_id not in [x.trip_route_id for x in TripRoute.trip_routes]:
                return cls.trip_route_id

