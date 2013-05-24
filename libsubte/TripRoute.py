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

class TripRoute(BaseObject):
    '''This is a group of trips that
    all share the same stops along a route'''
    def __init__(self, route, calendar, headsign, direction, path = None):
        BaseObject.__init__(self)

        self._route = weakref.ref(route)
        self._calendar = weakref.ref(calendar)

        self.direction = direction
        self.path = path

        self.wheelchair_accessible = 0

        self.trips = []

        self._stops = []

    route = property(lambda x: x._route(), None)
    calendar = property(lambda x: x._calendar(), None)
    stops = property(lambda x: x._stops[:], None)

    def add_trip(self):
        trip = Trip('', self.route, self.calendar)

        # add the stops
        for stop in self._stops:
            trip.add_stop(TripStop(stop))

        self._trips.append(trip)

        return trip

    def add_stop(self, stop):
        self._stops.append(stop)

        # for all our trips
        for trip in self.trips:
            t = TripStop(stop)
            trip.add_stop(t)

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
