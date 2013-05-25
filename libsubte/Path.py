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

class Path(BaseObject):
    '''Path is a set of coordinates along which a route follows.
    This translates into a shape in GTFS data.'''
    paths = []
    path_id = 0

    def __init__(self, name, coords = None):
        BaseObject.__init__(self)

        self.path_id = Path.new_id()
        self.name = name
        self.coords = coords

        # add us
        Path.paths.append(self)

    def destroy(self):
        self.name = None
        self.coords = []

        try:
            Path.paths.remove(self)
        except ValueError, e:
            pass

    def write(self, f):
        if self.coords is None:
            return

        from TripRoute import TripRoute
        found = False
        for r in TripRoute.trip_routes:
            if r.path == self:
                found = True
                break

        if not found: # don't write us out
            return

        for i, coord in enumerate(self.coords):
            self._write(f, '%s,%s,%s,%s,%s\n',
                        self.path_id,
                        coord[0], coord[1],
                        (i+1), '')

    @classmethod
    def get(cls, path_id):
        for path in cls.paths:
            if path.path_id == path_id:
                return path
        return None

    @classmethod
    def new_id(cls):
        while True:
            cls.path_id += 1
            if cls.path_id not in [x.path_id for x in Path.paths]:
                return cls.path_id

    @classmethod
    def write_paths(cls, directory = '.'):
        f = open(os.path.join(directory, 'shapes.txt'), 'w')
        # header
        f.write('shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled\n')
        for p in cls.paths:
            p.write(f)
        f.close()
