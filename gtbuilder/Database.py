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

import xml.etree.ElementTree as ElementTree

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
            r.trips = [] # !mwd - Weakref HACK!
            d.append(r)
    
        #for t in Trip.trips:
        #    d.append(t)

        f = open(fname, 'w')
        pickle.dump(d, f)
        f.close()

        # save the xml
        root = ElementTree.Element('gtbuilder')

        # the agencies
        for a in Agency.agencies:
            node = ElementTree.SubElement(root, 'Agency')
            node.attrib['id'] = '%s' % a.agency_id
            e = ElementTree.SubElement(node, 'name')
            e.text = a.name
            e = ElementTree.SubElement(node, 'url')
            e.text = a.url
            e = ElementTree.SubElement(node, 'timezone')
            e.text = a.timezone
            e = ElementTree.SubElement(node, 'language')
            e.text = a.language
            e = ElementTree.SubElement(node, 'phone')
            e.text = a.phone
            e = ElementTree.SubElement(node, 'fare_url')
            e.text = a.fare_url
        # the calendars
        for c in Calendar.calendars:
            node = ElementTree.SubElement(root, 'Calendar')
            node.attrib['id'] = '%s' % c.calendar_id
            e = ElementTree.SubElement(node, 'name')
            e.text = c.name
            e = ElementTree.SubElement(node, 'days')
            e.text = ' '.join([str(x) for x in c.days])
            e = ElementTree.SubElement(node, 'start_date')
            e.text = '%s' % (c.start_date or '')
            e = ElementTree.SubElement(node, 'end_date')
            e.text = '%s' % (c.end_date or '')
        # the stops
        for s in Stop.stops:
            node = ElementTree.SubElement(root, 'Stop')
            node.attrib['id'] = '%s' % s.stop_id
            e = ElementTree.SubElement(node, 'code')
            e.text = s.code or ''
            e = ElementTree.SubElement(node, 'name')
            e.text = s.name or ''
            e = ElementTree.SubElement(node, 'description')
            e.text = s.description or ''
            e = ElementTree.SubElement(node, 'latitude')
            e.text = '%s' % (s.latitude or '')
            e = ElementTree.SubElement(node, 'longitude')
            e.text = '%s' % (s.longitude or '')
            e = ElementTree.SubElement(node, 'zone_id')
            e.text = '%s' % (s.zone_id or '')
            e = ElementTree.SubElement(node, 'url')
            e.text = '%s' % (s.url or '')
            e = ElementTree.SubElement(node, 'location_type')
            e.text = '%s' % (s.location_type or '')
            e = ElementTree.SubElement(node, 'parent_station')
            e.text = '%s' % (s.parent_station or '')

        # the routes
        for r in Route.routes:
            node = ElementTree.SubElement(root, 'Route')
            node.attrib['id'] = '%s' % r.route_id
            e = ElementTree.SubElement(node, 'agency_id')
            e.text = '%s' % r.agency.agency_id
            e = ElementTree.SubElement(node, 'short_name')
            e.text = r.short_name or ''
            e = ElementTree.SubElement(node, 'long_name')
            e.text = r.long_name or ''
            e = ElementTree.SubElement(node, 'description')
            e.text = r.description or ''
            e = ElementTree.SubElement(node, 'route_type')
            e.text = '%s' % (r.route_type or '')
            e = ElementTree.SubElement(node, 'url')
            e.text = '%s' % (r.url or '')
            e = ElementTree.SubElement(node, 'color')
            e.text = '%s' % (r.color or '')
            e = ElementTree.SubElement(node, 'text_color')
            e.text = '%s' % (r.text_color or '')
            # this routes stops
            stop_node = ElementTree.SubElement(node, 'Stops')
            for s in r.stops:
                n = ElementTree.SubElement(stop_node, 'Stop')
                n.attrib['id'] = '%s' % s.stop_id
            
        # the trips
        print 'trips=', Trip.trips
        for t in Trip.trips:
            node = ElementTree.SubElement(root, 'Trip')
            node.attrib['id'] = '%s' % t.trip_id
            e = ElementTree.SubElement(node, 'name')
            e.text = '%s' % t.name
            e = ElementTree.SubElement(node, 'calendar_id')
            e.text = '%s' % t.calendar.calendar_id
            e = ElementTree.SubElement(node, 'route_id')
            e.text = '%s' % t.route.route_id
            # this trips stops
            stop_node = ElementTree.SubElement(node, 'TripStops')
            for k, v in t.stops.iteritems():
                n = ElementTree.SubElement(stop_node, 'TripStop')
                e = ElementTree.SubElement(n, 'stop_id')
                e.text = '%s' % v.stop.stop_id
                e = ElementTree.SubElement(n, 'arrival')
                e.text = '%s' % (v.arrival or '')
                e = ElementTree.SubElement(n, 'departure')
                e.text = '%s' % (v.departure or '')


        # make a tree and save it
        self.__indent(root)
        tree = ElementTree.ElementTree(root)
        d = os.path.dirname(fname)
        tree.write(os.path.join(d, '.gtbuilder.xml'), encoding = 'UTF-8')

    def __indent(self, elem, level = 0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            for elem in elem:
                self.__indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i


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
