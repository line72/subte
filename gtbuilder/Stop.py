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

# import sqlobject

# class Stop(sqlobject.SQLObject):
#     code = sqlobject.StringCol(default = None)
#     name = sqlobject.StringCol(default = None)
#     description = sqlobject.StringCol(default = None)
#     latitude = sqlobject.FloatCol()
#     longitude = sqlobject.FloatCol()
#     zone_id = sqlobject.StringCol(default = 'zone1') # !mwd - should be a reference
#     url = sqlobject.StringCol(default = None)
#     location_type = sqlobject.EnumCol(enumValues = ('STATION', 'STOP'), default = 'STOP')
#     parent_station = sqlobject.StringCol(default = None)
#     routes = sqlobject.RelatedJoin('Route')
#     trip_stops = sqlobject.RelatedJoin('TripStop')


import weakref

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

        # add us
        Stop.stops.append(self)

    def write(self, f):
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
    def write_stops(cls):
        f = open('stops.txt', 'w')
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
