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
import time
import datetime
import weakref
import csv

from BaseObject import BaseObject
from Trip import Trip
from Stop import Stop
from Agency import Agency

class Route(BaseObject):
    routes = []
    route_id = 0

    def __init__(self, agency = None, short_name = '',
                 long_name = '', description = '',
                 route_type = None, url = '', color = None, text_color = None):
        BaseObject.__init__(self)

        self.route_id = Route.new_id()
        self.agency = agency
        if agency is None:
            self.agency = Agency.agencies[0]
        self.short_name = short_name
        self.long_name = long_name
        self.description = description
        self.route_type = route_type
        self.url = url
        self.color = color
        self.text_color = text_color

        self.trip_routes = []

        # add us
        Route.routes.append(self)

    def destroy(self):
        #self.stops = []
        self.trip_routes = []
        self.agency = None

        try:
            Route.routes.remove(self)
        except ValueError:
            pass

    def add_trip_route(self, trip_route):
        self.trip_routes.append(trip_route)

    def remove_trip_route(self, trip_route):
        try: self.trip_routes.remove(trip_route)
        except ValueError, e:
            pass

    def get_id(self):
        if self.gtfs_id:
            return self.gtfs_id
        return self.route_id

    def write(self, f):
        self._write(f, '%s,%s,%s,%s,%s,%s,%s,%s,%s\n',
                    self.get_id(), self.agency.get_id(),
                    self.short_name or '', self.long_name or '',
                    self.description or '', self.route_type or 3,
                    self.url or '', self.color or '',
                    self.text_color or '')

    @classmethod
    def clear(cls):
        for route in cls.routes:
            route.destroy()

        cls.routes = []
        cls.route_id = 0

    @classmethod
    def get(cls, route_id):
        for route in cls.routes:
            if route.route_id == route_id:
                return route
        return None
        
    @classmethod
    def get_by_gtfs_id(cls, gtfs_id):
        for route in cls.routes:
            if route.gtfs_id == gtfs_id:
                return route
        return None

    @classmethod
    def new_id(cls):
        while True:
            cls.route_id += 1
            if cls.route_id not in [x.route_id for x in Route.routes]:
                return cls.route_id

    @classmethod
    def write_routes(cls, directory = '.'):
        f = open(os.path.join(directory, 'routes.txt'), 'w')
        # header
        f.write('route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color\n')
        for r in cls.routes:
            r.write(f)
        f.close()

    @classmethod
    def import_routes(cls, directory):
        try:
            f = open(os.path.join(directory, 'routes.txt'), 'rb')
            reader = csv.reader(f)

            mappings = {'agency_id': ('agency', lambda x: Agency.get_by_gtfs_id(x)),
                        'route_short_name': ('short_name', lambda x: x),
                        'route_long_name': ('long_name', lambda x: x),
                        'route_desc': ('description', lambda x: x),
                        'route_type': ('route_type', lambda x: int(x)),
                        'route_url': ('url', lambda x: x),
                        'route_color': ('color', lambda x: x),
                        'route_text_color': ('text_color', lambda x: x),
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
                # create the route
                route = Route(**kw)
                # set the id
                route.gtfs_id = BaseObject.unquote(l2[r_headers['route_id']])

        except IOError, e:
            print >> sys.stderr, 'Unable to open routes.txt:', e

