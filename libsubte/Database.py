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

import sys
import os

import weakref
import cPickle as pickle
import string
import random

import xml.etree.ElementTree as ElementTree
import xml.parsers.expat

from Route import Route
from Stop import Stop
from Trip import Trip, TripStop
from TripRoute import TripRoute
from Calendar import Calendar
from Agency import Agency
from Path import Path
from Picture import Picture

class Database(object):
    def load(self, fname):
        try:
            d = os.path.dirname(fname)
            tree = ElementTree.parse(os.path.join(d, '.subte.xml'))

            for agency_node in tree.getroot().findall('Agency'):
                agency_id = agency_node.get('id', Agency.new_id())
                name = agency_node.findtext('name')
                url = agency_node.findtext('url')
                timezone = agency_node.findtext('timezone')
                language = agency_node.findtext('language')
                phone = agency_node.findtext('phone')
                fare_url = agency_node.findtext('fare_url')

                a = Agency(name = name, url = url, timezone = timezone, language = language,
                           phone = phone, fare_url = fare_url)
                a.agency_id = int(agency_id)
            
            for calendar_node in tree.getroot().findall('Calendar'):
                calendar_id = calendar_node.get('id', Calendar.new_id())
                name = calendar_node.findtext('name')
                days = calendar_node.findtext('days')
                start_date = calendar_node.findtext('start_date')
                end_date = calendar_node.findtext('end_date')

                days = [int(x) for x in days.split()]
                c = Calendar(service_name = name, monday = days[0],
                             tuesday = days[1], wednesday = days[2],
                             thursday = days[3], friday = days[4],
                             saturday = days[5], sunday = days[6],
                             start_date = start_date, end_date = end_date)
                c.calendar_id = int(calendar_id)

            for stop_node in tree.getroot().findall('Stop'):
                stop_id = stop_node.get('id', Stop.new_id())
                code = stop_node.findtext('code')
                name = stop_node.findtext('name')
                description = stop_node.findtext('description')
                latitude = stop_node.findtext('latitude')
                longitude = stop_node.findtext('longitude')
                zone_id = stop_node.findtext('zone_id')
                url = stop_node.findtext('url')
                location_type = stop_node.findtext('location_type')
                parent_station = stop_node.findtext('parent_station')

                try: location_type = int(location_type)
                except: pass

                try:
                    s = Stop(code = code, name = name, description = description,
                             latitude = float(latitude), longitude = float(longitude),
                             zone_id = zone_id, url = url, location_type = location_type,
                             parent_station = parent_station)
                    s.stop_id = int(stop_id)
                except Exception, e:
                    print >> sys.stderr, 'Error loading stop', name, e

            for path_node in tree.getroot().findall('Path'):
                path_id = path_node.get('id', Path.new_id())
                name = path_node.findtext('name')

                coords_node = path_node.find('coordinates')
                coords = []
                for coord_node in coords_node.findall('Coordinate'):
                    try:
                        sequence = int(coord_node.get('sequence', -1))
                        lat = float(coord_node.get('lat', 0.0))
                        lon = float(coord_node.get('lon', 0.0))
                        coords.append((lat, lon))
                    except Exception, e:
                        print >> sys.stderr, 'Invalid coordinate path %s: %s' % (name, e)

                try:
                    p = Path(name = name, coords = coords)
                    p.path_id = int(path_id)
                except Exception, e:
                    print >> sys.stderr, 'Error loading path', name, e

            for route_node in tree.getroot().findall('Route'):
                route_id = route_node.get('id', Route.new_id())
                agency_id = route_node.findtext('agency_id')
                short_name = route_node.findtext('short_name')
                long_name = route_node.findtext('long_name')
                description = route_node.findtext('description')
                route_type = route_node.findtext('route_node')
                url = route_node.findtext('url')
                color = route_node.findtext('color')
                text_color = route_node.findtext('text_color')

                agency_id = int(agency_id)
                r = Route(agency = Agency.get(agency_id),
                          short_name = short_name, long_name = long_name,
                          description = description, route_type = route_type,
                          url = url, color = color, text_color = text_color)
                r.route_id = int(route_id)

            for trip_route_node in tree.getroot().findall('TripRoute'):
                trip_route_id = trip_route_node.get('id', TripRoute.new_id())
                name = trip_route_node.findtext('name')
                route_id = trip_route_node.findtext('route_id')
                calendar_id = trip_route_node.findtext('calendar_id')
                headsign = trip_route_node.findtext('headsign')
                direction = trip_route_node.findtext('direction')
                path_id = trip_route_node.findtext('path_id')

                route = Route.get(int(route_id))
                calendar = Calendar.get(int(calendar_id))
                path = None
                if path_id != '':
                    path = Path.get(int(path_id))

                tr = TripRoute(name, route, calendar, headsign, int(direction), path)
                tr.trip_route_id = int(trip_route_id)
                route.add_trip_route(tr)

                # stops
                stops_node = trip_route_node.find('Stops')
                for stop_node in stops_node.findall('Stop'):
                    stop_id = stop_node.get('id')

                    stop = Stop.get(int(stop_id))
                    tr.add_stop(stop)

                # trips
                trips_node = trip_route_node.find('Trips')
                for trip_node in trips_node.findall('Trip'):
                    trip_id = trip_node.get('id')

                    trip = tr.add_trip()
                    trip.trip_id = int(trip_id)


            for trip_node in tree.getroot().findall('Trip'):
                trip_id = trip_node.get('id', Trip.new_id())
                name = trip_node.findtext('name')
                calendar_id = trip_node.findtext('calendar_id')
                route_id = trip_node.findtext('route_id')

                route = Route.get(int(route_id))

                trip = Trip.get(int(trip_id))
                trip.name = name

                # trip stops
                trip_stops_node = trip_node.find('TripStops')
                for i, trip_stop_node in enumerate(trip_stops_node.findall('TripStop')):
                    stop_id = trip_stop_node.findtext('stop_id')
                    arrival = trip_stop_node.findtext('arrival')
                    departure = trip_stop_node.findtext('departure')

                    stop = Stop.get(int(stop_id))
                    #trip_stop = trip.get_stop(stop)
                    trip_stop = trip.stops[i]
                    if trip_stop.stop != stop:
                        raise Exception("TripStop doesn't match stop")

                    trip_stop.arrival = arrival
                    trip_stop.departure = departure

                # blocks
                previous_trip = trip_node.findtext('previous_block')
                next_trip = trip_node.findtext('next_block')

                try:
                    previous_block = Trip.get(int(previous_trip))
                    trip.previous_block = previous_block
                except Exception, e: pass

                try:
                    next_block = Trip.get(int(next_trip))
                    trip.next_block = next_block
                except Exception, e: pass

            for picture_node in tree.getroot().findall('Picture'):
                picture_id = picture_node.get('id', Picture.new_id())
                image = picture_node.findtext('image')
                stop_id = picture_node.findtext('stop_id', -1)
                ignored = picture_node.findtext('ignored')
                latitude = picture_node.findtext('latitude')
                longitude = picture_node.findtext('longitude')
                orientation = picture_node.findtext('orientation')

                try:
                    stop_id = int(stop_id)
                    ignored = bool(int(ignored))

                    stop = Stop.get(stop_id)

                    if latitude is not None and longitude is not None and orientation is not None:
                        p = Picture(image, latitude = float(latitude), longitude = float(longitude), orientation = int(orientation))
                    else:
                        p = Picture(image)

                    if stop:
                        stop.add_picture(p)

                    p.picture_id = int(picture_id)
                except Exception, e:
                    print >> sys.stderr, 'Invalid picture: %s' % e

        except (IOError, xml.parsers.expat.ExpatError), e:
            print 'Error loading saved state', e
            return
            

    def save(self, fname):
        # save the xml
        root = ElementTree.Element('subte')

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

        # the trips
        for t in Trip.trips:
            node = ElementTree.SubElement(root, 'Trip')
            node.attrib['id'] = '%s' % t.trip_id
            e = ElementTree.SubElement(node, 'name')
            e.text = '%s' % t.name
            e = ElementTree.SubElement(node, 'calendar_id')
            e.text = '%s' % t.calendar.calendar_id
            e = ElementTree.SubElement(node, 'route_id')
            e.text = '%s' % t.trip_route.route.route_id
            # this trips stops
            stop_node = ElementTree.SubElement(node, 'TripStops')
            for rs in t.stops:
                v = rs
                n = ElementTree.SubElement(stop_node, 'TripStop')
                e = ElementTree.SubElement(n, 'stop_id')
                e.text = '%s' % v.stop.stop_id
                e = ElementTree.SubElement(n, 'arrival')
                e.text = '%s' % (v.arrival or '')
                e = ElementTree.SubElement(n, 'departure')
                e.text = '%s' % (v.departure or '')
            # blocks
            e = ElementTree.SubElement('previous_block')
            if t.previous_block:
                e.text = t.previous_block.trip_id
            else:
                e.text = ''

            e = ElementTree.SubElement('next_block')
            if t.next_block:
                e.text = t.next_block.trip_id
            else:
                e.text = ''            

        # the trip routes           
        for tr in TripRoute.trip_routes:
            node = ElementTree.SubElement(root, 'TripRoute')
            node.attrib['id'] = '%s' % tr.trip_route_id
            e = ElementTree.SubElement(node, 'name')
            e.text = '%s' % tr.name
            e = ElementTree.SubElement(node, 'route_id')
            e.text = '%s' % tr.route.route_id
            e = ElementTree.SubElement(node, 'calendar_id')
            e.text = '%s' % tr.calendar.calendar_id
            e = ElementTree.SubElement(node, 'headsign')
            e.text = '%s' % tr.headsign
            e = ElementTree.SubElement(node, 'direction')
            e.text = '%s' % tr.direction
            e = ElementTree.SubElement(node, 'path_id')
            if tr.path:
                e.text = '%s' % tr.path.path_id
            else:
                e.text = ''
            # stops
            stop_node = ElementTree.SubElement(node, 'Stops')
            for s in tr.stops:
                n = ElementTree.SubElement(stop_node, 'Stop')
                n.attrib['id'] = '%s' % s.stop_id
            # trips
            trip_node = ElementTree.SubElement(node, 'Trips')
            for t in tr.trips:
                n = ElementTree.SubElement(trip_node, 'Trip')
                n.attrib['id'] = '%s' % t.trip_id               

        # the paths
        for p in Path.paths:
            node = ElementTree.SubElement(root, 'Path')
            node.attrib['id'] = '%s' % p.path_id
            e = ElementTree.SubElement(node, 'name')
            e.text = '%s' % p.name
            coord_node = ElementTree.SubElement(node, 'coordinates')
            if p.coords:
                for j, coord in enumerate(p.coords):
                    n = ElementTree.SubElement(coord_node, 'Coordinate')
                    n.attrib['lat'] = '%s' % coord[0]
                    n.attrib['lon'] = '%s' % coord[1]
                    n.attrib['sequence'] = '%s' % j

        # the pictures
        for p in Picture.pictures:
            node = ElementTree.SubElement(root, 'Picture')
            node.attrib['id'] = '%s' % p.picture_id
            e = ElementTree.SubElement(node, 'image')
            e.text = '%s' % p.image
            e = ElementTree.SubElement(node, 'stop_id')
            e.text = '%s' % p.stop_id
            e = ElementTree.SubElement(node, 'ignored')
            e.text = '%s' % int(p.ignored)
            e = ElementTree.SubElement(node, 'latitude')
            e.text = '%s' % p._latitude
            e = ElementTree.SubElement(node, 'longitude')
            e.text = '%s' % p._longitude
            e = ElementTree.SubElement(node, 'orientation')
            e.text = '%s' % p.orientation

        # make a tree and save it
        self.__indent(root)
        tree = ElementTree.ElementTree(root)
        d = os.path.dirname(fname)
        tmpname = ''.join([random.choice(string.ascii_letters) for i in range(8)])
        # write out a temporary
        tree.write(os.path.join(d, tmpname), encoding = 'UTF-8')
        # make a backup
        try: os.rename(os.path.join(d, '.subte.xml'), os.path.join(d, '.subte.xml-bk'))
        except OSError, e: pass
        # move the temporary to the new
        try: os.rename(os.path.join(d, tmpname), os.path.join(d, '.subte.xml'))
        except OSError, e: pass

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
        Path.write_paths(directory)

"""
<?xml>
<subte version="1.0">
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
</subte>
"""
