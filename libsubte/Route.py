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
import time
import datetime
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

        #self.stops = []
        self.trip_routes = []

        #self.path = None

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

    #def add_stop(self, stop):
    #    self.stops.append(stop)

    # def remove_stop(self, stop):
    #     try:
    #         self.stops.remove(stop)

    #         for trip_route in self.trip_routes:
    #             trip_route.remove_stop(stop)

    #     except ValueError, e:
    #         pass

    def add_trip_route(self, trip_route):
        self.trip_routes.append(trip_route)

    def remove_trip_route(self, trip_route):
        try: self.trip_routes.remove(trip_route)
        except ValuError, e:
            pass

    # def set_path(self, p):
    #     self.path = p

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
    def write_routes(cls, directory = '.'):
        f = open(os.path.join(directory, 'routes.txt'), 'w')
        # header
        f.write('route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color\n')
        for r in cls.routes:
            r.write(f)
        f.close()


