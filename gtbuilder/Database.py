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
import cPickle as pickle

from Route import Route
from Stop import Stop
from Trip import Trip, TripStop
from Calendar import Calendar
from Agency import Agency

class Database(object):
    def load(self, fname):
        try:
            f = open(fname)
            d = pickle.load(f)
            f.close()

            for i in d:
                if isinstance(i, Agency):
                    Agency.agencies.append(i)
                elif isinstance(i, Calendar):
                    Calendar.calendars.append(i)
                elif isinstance(i, Stop):
                    Stop.stops.append(i)
                elif isinstance(i, Route):
                    Route.routes.append(i)
                elif isinstance(i, Trip):
                    Trip.trips.append(weakref.ref(i))
                else:
                    print 'unknown type', i

        except Exception, e:
            print 'error loading', e

    def save(self, fname):
        d = []

        for a in Agency.agencies:
            d.append(a)

        for c in Calendar.calendars:
            d.append(c)

        for s in Stop.stops:
            d.append(s)

        for r in Route.routes:
            d.append(r)
    
        for t in Trip.trips:
            d.append(t)

        f = open(fname, 'w')
        pickle.dump(d, f)
        f.close()

    @classmethod
    def export(cls, directory):
        Agency.write_agencies(directory)
        Calendar.write_calendars(directory)
        Stop.write_stops(directory)
        Route.write_routes(directory)
        Trip.write_trips(directory)

"""
<?xml>
<gtbuilder version="1.0">
  <stops>
    <stop>
      <id>0</id>
      <code>code</code>
      <name>name</name>
      <description>description</description>
      <latitude>33.23423</latitude>
      <longitude>-86.234</longitude>
      <zone_id>zone_id</zone_id>
      <url>http://</url>
      <location_type>0</location_type>
      <parent_station>0</parent_station>
    </stop>
  </stops>
</gtbuilder>
"""
