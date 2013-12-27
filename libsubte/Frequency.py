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
import weakref

from BaseObject import BaseObject

class Frequency(BaseObject):
    '''This holds a frequency trip'''

    frequencies = []
    frequency_id = 0

    def __init__(self, trip_route, start, end, headway):
        BaseObject.__init__(self)

        self.frequency_id = Frequency.new_id()
        
        self.start = start
        self.end = end
        self.headway = headway

        self._trip_route = weakref.ref(trip_route)

        # add us
        Frequency.frequencies.append(self)

    trip_route = property(lambda x: x._trip_route(), None)

    def destroy(self):
        try:
            Frequency.frequencies.remove(self)
        except ValueError, e:
            pass

    def write(self, f):
        self._write(f, '%s,%s,%s,%s,%s\n',
                    self.trip_route.trips[0].trip_id,
                    self.start, self.end, self.headway, 0)

    @classmethod
    def clear(cls):
        for frequency in cls.frequencies:
            frequency.destroy()

        cls.frequencies = []
        cls.frequency_id = 0
        
    @classmethod
    def get(cls, frequency_id):
        for frequency in cls.frequencies:
            if frequency.frequency_id == frequency_id:
                return frequency

        return None

    @classmethod
    def new_id(cls):
        while True:
            cls.frequency_id += 1
            if cls.frequency_id not in [x.frequency_id for x in Frequency.frequencies]:
                return cls.frequency_id

    @classmethod
    def write_frequencies(cls, directory = '.'):
        f = open(os.path.join(directory, 'frequencies.txt'), 'w')

        # header
        f.write('trip_id,start_time,end_time,headway_secs,exact_times\n')

        for frequency in cls.frequencies:
            frequency.write(f)
        f.close()

    @classmethod
    def import_frequencies(cls, directory):
        from Trip import Trip

        try:
            f = open(os.path.join(directory, 'frequencies.txt'), 'rb')
            reader = csv.reader(f)

            mappings = {'trip_id': ('trip_route', lambda x: Trip.get_by_gtfs_id(x).trip_route),
                        'start_time': ('start', lambda x: x),
                        'end_time': ('end', lambda x: x),
                        'headway_secs': ('headway', lambda x: x),
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
                # create the frequency
                frequency = Frequency(**kw)
                trip_route = frequency.trip_route.frequencies.append(frequency)

        except IOError, e:
            print >> sys.stderr, 'Unable to open frequencies.txt:', e
