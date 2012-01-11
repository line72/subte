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

import time
import datetime

# import sqlobject

# class Route(sqlobject.SQLObject):
#     agency = sqlobject.ForeignKey('Agency')
#     short_name = sqlobject.StringCol(default = None)
#     long_name = sqlobject.StringCol(default = None)
#     description = sqlobject.StringCol(default = None)
#     route_type = sqlobject.EnumCol(enumValues = ('BUS', 'SUBWAY'), default = 'BUS') #!mwd - add the rest
#     url = sqlobject.StringCol(default = None)
#     color = sqlobject.StringCol(default = None) # !mwd - what should this be?
#     text_color = sqlobject.StringCol(default = None) # !mwd - what should this be?
#     stops = sqlobject.RelatedJoin('Stop')
#     trips = sqlobject.MultipleJoin('Trip')


#     # perform an action when stops are added/deleted
#     # we must automatically add/remove trip stops
#     #  from our trips since there must be a 1:1 correlation
#     def addStop(self, s):
#         t = self._SO_addStop(s)

#         date = datetime.time(0, 0, 0)

#         for trip in self.trips:
#             ts = gtbuilder.TripStop(arrival = None)
#             ts.addStop(s)

#             trip.addTripStop(ts)

#         return t

#     def removeStop(self, s):
#         r = self._SO_removeStop(s)

#         for trip in self.trips:
#             ts = gtbuilder.TripStop.get(trip = trip,
#                                         stop = s)
#             if ts is not None:
#                 trip.removeTripStop(ts)

#         return r

#     # when we add a trip, automatically add all the trip stops to it
#     def addTrip(self, t):
#         print 'ADDTRIP, building stops'
#         r = self._SO_addTrip(t)

#         for s in self.stops:
#             t.addTripStop(gtbuilder.TripStop(arrival = None, stop = s))

#         return r

import weakref

from BaseObject import BaseObject
from Trip import Trip
from Stop import Stop

class Route(BaseObject):
    routes = []
    route_id = 0

    def __init__(self, agency = None, short_name = '',
                 long_name = '', description = '',
                 route_type = None, url = '', color = None, text_color = None):
        BaseObject.__init__(self)

        self.route_id = Route.new_id()
        self.agency = agency
        self.short_name = short_name
        self.long_name = long_name
        self.description = description
        self.route_type = route_type
        self.url = url
        self.color = color
        self.text_color = text_color

        self.stops = []
        self.trips = []

        # add us
        Route.routes.append(self)

    def add_stop(self, stop):
        self.stops.append(stop)

    def add_trip(self, name, calendar):
        trip = Trip(name, self, calendar)
        self.trips.append(trip)
    
        return trip

    def build_trips(self, csv, calendar, trip_name = None):
        '''build trips from a csv file.'''
        f = open(csv)
        stops = f.readline().strip().split(',')

        if trip_name is None:
            trip_name = csv[:-4] # remove the .csv

        for i, l in enumerate(f.readlines()):
            trip = self.add_trip('%s%d' % (trip_name, i), calendar)
            
            times = l.strip().split(',')

            previous_stop = ''
            for s, t in zip(stops, times):
                if t == '--': # skip
                    continue
                if s == previous_stop:
                    # set the departure time
                    trip.stops[-1].departure = t
                else:
                    # a blank time is ok, it just means
                    #  google will interpolate it
                    trip.add_stop(Stop.get_stop(s), t)
                
                previous_stop = s


    def write(self, f):
        self._write(f, '%s,%s,%s,%s,%s,%s,%s,%s,%s\n',
                    self.route_id, self.agency.agency_id,
                    self.short_name or '', self.long_name or '',
                    self.description or '', self.route_type or 3,
                    self.url or '', self.color or '',
                    self.text_color or '')

    @classmethod
    def get(cls, route_id):
        for route in cls.routes:
            if route.route_id == route_id:
                return route
        return None
        
    @classmethod
    def new_id(cls):
        while True:
            cls.route_id += 1
            if cls.route_id not in [x.route_id for x in Route.routes]:
                return cls.route_id

    @classmethod
    def write_routes(cls):
        f = open('routes.txt', 'w')
        # header
        f.write('route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color\n')
        for r in cls.routes:
            r.write(f)
        f.close()


