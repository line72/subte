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
import csv

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

    def get_id(self):
        if self.gtfs_id:
            return self.gtfs_id
        return self.path_id

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
                        self.get_id(),
                        coord[0], coord[1],
                        (i+1), '')

    @classmethod
    def clear(cls):
        for path in cls.paths:
            path.destroy()

        cls.paths = []
        cls.path_id = 0

    @classmethod
    def get(cls, path_id):
        for path in cls.paths:
            if path.path_id == path_id:
                return path
        return None

    @classmethod
    def get_by_gtfs_id(cls, gtfs_id):
        for path in cls.paths:
            if path.gtfs_id == gtfs_id:
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

    @classmethod
    def import_paths(cls, directory):
        try:
            f = open(os.path.join(directory, 'shapes.txt'), 'rb')
            reader = csv.reader(f)

            shapes = {}

            # create a headers with an index
            headers = reader.next()
            r_headers = dict([(x, i) for i, x in enumerate(headers)])

            for l2 in reader:
                if len(l2) != len(headers):
                    print >> sys.stderr, 'Invalid line', l2, headers
                    continue

                sid = l2[r_headers['shape_id']]
                lat = float(l2[r_headers['shape_pt_lat']])
                lon = float(l2[r_headers['shape_pt_lon']])
                seq = int(l2[r_headers['shape_pt_sequence']])
                #dis = float(l2[r_headers['shape_dist_traveled']])

                if sid not in shapes:
                    shapes[sid] = {'coords': [],
                                   'distance': []}

                #!mwd - we don't handle the dist travelled correctly yet
                #!mwd - we should actually use the sequnce to verify
                #  these are in order instead of just appending them
                shapes[sid]['coords'].append((lat, lon))
                #shapes[sid]['distance'].append(dis)

            # now create the paths
            for k, v in shapes.iteritems():
                path = Path(k, v['coords'])
                path.gtfs_id = k

        except IOError, e:
            print >> sys.stderr, 'Unable to open paths.txt:', e

