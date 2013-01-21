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

from BaseObject import BaseObject

class Stop(BaseObject):
    stops = []
    stop_id = 0

    def __init__(self, code = None, name = None,
                 description = None, latitude = None, longitude = None,
                 zone_id = None, url = None, location_type = 0, parent_station = None):
        BaseObject.__init__(self)

        self.stop_id = Stop.new_id()
        self.code = code
        self.name = name
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self.zone_id = zone_id
        self.url = url
        self.location_type = location_type
        self.parent_station = parent_station

        self.pictures = []

        # add us
        Stop.stops.append(self)

    @property
    def routes(self):
        from Route import Route

        r = []
        for route in Route.routes:
            if self in route.stops:
                r.append(route)

        return r

    def is_orphan(self):
        '''Nothing is using this stop'''
        from Route import Route
        for route in Route.routes:
            if self in route.stops:
                return False

        return True

    def merge_with(self, stop):
        '''Merge stop into us'''
        from Route import Route
        from Trip import Trip, TripStop

        # collect their pictures
        for pic in stop.pictures:
            self.add_picture(pic)

        # any routes that have them as a stop
        #  need to be changed to us
        for route in Route.routes:
            if stop in route.stops:
                i = route.stops.index(stop)
                # insert us
                route.stops.insert(i, self)
                # remove the original
                route.stops.remove(stop)

                # any trips that have them as a stop
                #  need to be changed to us
                for trip in route.trips:
                    if stop in trip.stops:
                        trip.stops[self] = trip.stops[stop]
                        trip.stops.pop(stop)

    def add_picture(self, p):
        if p in self.pictures:
            return

        # A picture can only be associated with
        #  a single stop
        if p.stop:
            p.stop.remove_picture(p)

        self.pictures.append(p)
        p.stop = self

    def remove_picture(self, p):
        try: self.pictures.remove(p)
        except ValueError, e: pass

    def destroy(self):
        # see if we are used by any routes
        #  and if so, we can't be deleted
        if not self.is_orphan:
            raise Exception('Stop is in use')

        for i in self.pictures:
            i.ignored = True

        try:
            Stop.stops.remove(self)
        except ValueError:
            pass

    def write(self, f):
        if self.is_orphan(): # skip us
            return

        self._write(f, '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n',
                    self.stop_id, self.code,
                    self.name, self.description,
                    self.latitude, self.longitude,
                    self.zone_id, self.url,
                    self.location_type or 0,
                    self.parent_station)

    @classmethod
    def load_stops(cls, filename):
        stops = []

        f = open(filename)
        title = f.readline()

        for l in f.readlines():
            info = l.strip().split(',')

            stops.append(Stop(stop_id = info[0],
                              name = info[1],
                              description = info[2],
                              latitude = float(info[3]),
                              longitude = float(info[4]),
                              zone_id = info[5]))

        return stops

    @classmethod
    def get(cls, stop_id):
        for stop in cls.stops:
            if stop.stop_id == stop_id:
                return stop
        return None

    @classmethod
    def new_id(cls):
        while True:
            cls.stop_id += 1
            if cls.stop_id not in [x.stop_id for x in Stop.stops]:
                return cls.stop_id
        
    @classmethod
    def write_stops(cls, directory = '.'):
        f = open(os.path.join(directory, 'stops.txt'), 'w')
        # header
        f.write('stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,location_type,parent_station\n')
        for s in cls.stops:
            s.write(f)
        f.close()

if __name__ == '__main__':
    s1 = Stop('central', '', 'Central Station', '',
              33.511878, -86.808826, 'zone1', '', 0, '')
    s2 = Stop('summit', '', 'Summit', 'Summit Shopping Center',
              33.44800, -86.73103, 'zone1', '', 0, '')

    s1 = None

    Stop.write_stops()
