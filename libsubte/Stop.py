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
    def trip_routes(self):
        from TripRoute import TripRoute

        r = []
        for tr in TripRoute.trip_routes:
            if self in tr.stops:
                r.append(tr)

        return r

    def is_orphan(self):
        '''Nothing is using this stop'''
        from TripRoute import TripRoute
        for tr in TripRoute.trip_routes:
            if self in tr.stops:
                return False

        return True

    def merge_with(self, stop):
        '''Merge stop into us'''
        from TripRoute import TripRoute
        from Trip import Trip, TripStop

        # collect their pictures
        for pic in stop.pictures:
            self.add_picture(pic)

        # any routes that have them as a stop
        #  need to be changed to us
        for tr in TripRoute.trip_routes:
            if stop in tr.stops:
                i = tr.stops.index(stop)
                # insert us
                tr.insert_stop_at(i, self)
                # remove the original
                i = tr.stops.index(stop)
                tr.remove_stop_at(i)

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
    def clear(cls):
        for stop in cls.stops:
            stop.destroy()

        cls.stops = []
        cls.stop_id = 0

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

    @classmethod
    def import_stops(cls, directory):
        try:
            f = open(os.path.join(directory, 'stops.txt'), 'r')

            mappings = {'stop_code': ('code', lambda x: x),
                        'stop_name': ('name', lambda x: x),
                        'stop_desc': ('description', lambda x: x),
                        'stop_lat': ('latitude', lambda x: float(x)),
                        'stop_lon': ('longitude', lambda x: float(x)),
                        'zone_id': ('zone_id', lambda x: x),
                        'stop_url': ('url', lambda x: x),
                        'location_type': ('location_type', lambda x: int(x)),
                        'parent_station': ('parent_station', lambda x: x),
                    }

            header_l = f.readline()
            # create a headers with an index
            headers = header_l.strip().split(',')
            r_headers = dict([(x, i) for i, x in enumerate(headers)])

            for l in f.readlines():
                l2 = l.strip().split(',')
                if len(l2) != len(headers):
                    print >> sys.stderr, 'Invalid line', l, l2, headers
                    continue
                
                kw = {}
                for i, a in enumerate(l2):
                    key = headers[i]
                    if key in mappings:
                        kw[mappings[key][0]] = mappings[key][1](BaseObject.unquote(a))
                # create the stop
                stop = Stop(**kw)
                # set the id
                stop.stop_id = BaseObject.unquote(l2[r_headers['stop_id']])

        except IOError, e:
            print >> sys.stderr, 'Unable to open stops.txt:', e


if __name__ == '__main__':
    s1 = Stop('central', '', 'Central Station', '',
              33.511878, -86.808826, 'zone1', '', 0, '')
    s2 = Stop('summit', '', 'Summit', 'Summit Shopping Center',
              33.44800, -86.73103, 'zone1', '', 0, '')

    s1 = None

    Stop.write_stops()
