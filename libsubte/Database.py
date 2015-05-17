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
from itertools import groupby

import xml.etree.ElementTree as ElementTree
import xml.parsers.expat
import json

from Route import Route
from Stop import Stop
from Trip import Trip, TripStop
from TripRoute import TripRoute
from Calendar import Calendar
from Agency import Agency
from Path import Path
from Picture import Picture
from Frequency import Frequency

class Database(object):
    def __init__(self):
        self._dbname = None
        self._is_open = False

    dbname = property(lambda x: x._dbname, None)
    is_open = property(lambda x: x._is_open, None)

    def is_empty(self):
        if len(Agency.agencies) > 0:
            return False
        if len(Calendar.calendars) > 0:
            return False
        if len(Stop.stops) > 0:
            return False
        if len(Path.paths) > 0:
            return False
        if len(Route.routes) > 0:
            return False
        if len(TripRoute.trip_routes) > 0:
            return False
        if len(Trip.trips) > 0:
            return False
        if len(Frequency.frequencies) > 0:
            return False
        if len(Picture.pictures) > 0:
            return False

        return True

    def load(self, fname):
        try:
            tree = ElementTree.parse(fname)

            for agency_node in tree.getroot().findall('Agency'):
                agency_id = agency_node.get('id', Agency.new_id())
                gtfs_id = agency_node.get('gtfs_id', None)
                name = agency_node.findtext('name')
                url = agency_node.findtext('url')
                timezone = agency_node.findtext('timezone')
                language = agency_node.findtext('language')
                phone = agency_node.findtext('phone')
                fare_url = agency_node.findtext('fare_url')

                a = Agency(name = name, url = url, timezone = timezone, language = language,
                           phone = phone, fare_url = fare_url)
                a.agency_id = int(agency_id)
                a.gtfs_id = gtfs_id
            
            for calendar_node in tree.getroot().findall('Calendar'):
                calendar_id = calendar_node.get('id', Calendar.new_id())
                gtfs_id = calendar_node.get('gtfs_id', None)
                name = calendar_node.findtext('name')
                days = calendar_node.findtext('days')
                start_date = calendar_node.findtext('start_date')
                end_date = calendar_node.findtext('end_date')
                added_excn = calendar_node.findtext('added_excn') or ''
                remov_excn = calendar_node.findtext('remov_excn') or ''

                days = [int(x) for x in days.split()]
                c = Calendar(service_name = name, monday = days[0],
                             tuesday = days[1], wednesday = days[2],
                             thursday = days[3], friday = days[4],
                             saturday = days[5], sunday = days[6],
                             start_date = start_date, end_date = end_date,
                             added_excn = added_excn.split(),
                             remov_excn = remov_excn.split())
                c.calendar_id = int(calendar_id)
                c.gtfs_id = gtfs_id

            for stop_node in tree.getroot().findall('Stop'):
                stop_id = stop_node.get('id', Stop.new_id())
                gtfs_id = stop_node.get('gtfs_id', None)
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
                    s.gtfs_id = gtfs_id
                except Exception, e:
                    print >> sys.stderr, 'Error loading stop', name, e

            for path_node in tree.getroot().findall('Path'):
                path_id = path_node.get('id', Path.new_id())
                gtfs_id = path_node.get('gtfs_id', None)
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
                    p.gtfs_id = gtfs_id
                except Exception, e:
                    print >> sys.stderr, 'Error loading path', name, e

            for route_node in tree.getroot().findall('Route'):
                route_id = route_node.get('id', Route.new_id())
                gtfs_id = route_node.get('gtfs_id', None)
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
                r.gtfs_id = gtfs_id

            for trip_route_node in tree.getroot().findall('TripRoute'):
                trip_route_id = trip_route_node.get('id', TripRoute.new_id())
                gtfs_id = trip_route_node.get('gtfs_id', None)
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
                tr.gtfs_id = gtfs_id
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
                gtfs_id = trip_node.get('gtfs_id', None)
                name = trip_node.findtext('name')
                calendar_id = trip_node.findtext('calendar_id')
                route_id = trip_node.findtext('route_id')

                route = Route.get(int(route_id))

                trip = Trip.get(int(trip_id))
                trip.name = name
                trip.gtfs_id = gtfs_id

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

                # !mwd - no need to set previous blocks
                #  since setting the next block automatically
                #  sets previously blocks
                #try:
                #    previous_block = Trip.get(int(previous_trip))
                #    trip.previous_block = previous_block
                #except Exception, e: pass

                try:
                    next_block = Trip.get(int(next_trip))
                    trip.next_block = next_block
                except Exception, e: pass

            for frequency_node in tree.getroot().findall('Frequency'):
                frequency_id = frequency_node.get('id', Frequency.new_id())
                gtfs_id = frequency_node.get('gtfs_id', None)
                trip_route_id = frequency_node.findtext('trip_route_id')
                start = frequency_node.findtext('start')
                end = frequency_node.findtext('end')
                headway = frequency_node.findtext('headway')

                trip_route = TripRoute.get(int(trip_route_id))

                frequency = trip_route.add_frequency(start, end, headway)
                frequency.frequency_id = int(frequency_id)
                frequency.gtfs_id = gtfs_id


            for picture_node in tree.getroot().findall('Picture'):
                picture_id = picture_node.get('id', Picture.new_id())
                relative_image = picture_node.findtext('image')
                stop_id = picture_node.findtext('stop_id', -1)
                ignored = picture_node.findtext('ignored')
                latitude = picture_node.findtext('latitude')
                longitude = picture_node.findtext('longitude')
                orientation = picture_node.findtext('orientation')

                # update the image with the full path
                dirname = os.path.dirname(fname)
                image = os.path.join(dirname, relative_image)

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

            self._dbname = fname
            self._is_open = True

        except (IOError, xml.parsers.expat.ExpatError), e:
            print 'Error loading saved state', e
            return
            
    def save_as(self, fname):
        self._dbname = fname
        self._is_open = True

        return self.save()

    def save(self):
        if self.dbname is None or self.is_open is False:
            return False

        # save the xml
        root = ElementTree.Element('subte')

        # the agencies
        for a in Agency.agencies:
            node = ElementTree.SubElement(root, 'Agency')
            node.attrib['id'] = '%s' % a.agency_id
            if a.gtfs_id:
                node.attrib['gtfs_id'] = '%s' % a.gtfs_id
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
            if c.gtfs_id:
                node.attrib['gtfs_id'] = '%s' % c.gtfs_id
            e = ElementTree.SubElement(node, 'name')
            e.text = c.name
            e = ElementTree.SubElement(node, 'days')
            e.text = ' '.join([str(x) for x in c.days])
            e = ElementTree.SubElement(node, 'start_date')
            e.text = '%s' % (c.start_date or '')
            e = ElementTree.SubElement(node, 'end_date')
            e.text = '%s' % (c.end_date or '')
            e = ElementTree.SubElement(node, 'added_excn')
            e.text = ' '.join(c.added_excn)
            e = ElementTree.SubElement(node, 'remov_excn')
            e.text = ' '.join(c.remov_excn)
        # the stops
        for s in Stop.stops:
            node = ElementTree.SubElement(root, 'Stop')
            node.attrib['id'] = '%s' % s.stop_id
            if s.gtfs_id:
                node.attrib['gtfs_id'] = '%s' % s.gtfs_id
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
            if r.gtfs_id:
                node.attrib['gtfs_id'] = '%s' % r.gtfs_id
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
            if t.gtfs_id:
                node.attrib['gtfs_id'] = '%s' % t.gtfs_id
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
            e = ElementTree.SubElement(node, 'previous_block')
            if t.previous_block:
                e.text = '%s' % t.previous_block.trip_id
            else:
                e.text = ''

            e = ElementTree.SubElement(node, 'next_block')
            if t.next_block:
                e.text = '%s' % t.next_block.trip_id
            else:
                e.text = ''            

        # the trip routes           
        for tr in TripRoute.trip_routes:
            node = ElementTree.SubElement(root, 'TripRoute')
            node.attrib['id'] = '%s' % tr.trip_route_id
            if tr.gtfs_id:
                node.attrib['gtfs_id'] = '%s' % tr.gtfs_id
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

        # the frequencies
        for f in Frequency.frequencies:
            node = ElementTree.SubElement(root, 'Frequency')
            node.attrib['id'] = '%s' % f.frequency_id
            if f.gtfs_id:
                node.attrib['gtfs_id'] = '%s' % f.gtfs_id
            e = ElementTree.SubElement(node, 'trip_route_id')
            e.text = '%s' % f.trip_route.trip_route_id
            e = ElementTree.SubElement(node, 'start')
            e.text = '%s' % f.start
            e = ElementTree.SubElement(node, 'end')
            e.text = '%s' % f.end
            e = ElementTree.SubElement(node, 'headway')
            e.text = '%s' % f.headway

        # the paths
        for p in Path.paths:
            node = ElementTree.SubElement(root, 'Path')
            node.attrib['id'] = '%s' % p.path_id
            if p.gtfs_id:
                node.attrib['gtfs_id'] = '%s' % p.gtfs_id
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
            image = p.image
            dirname = os.path.dirname(self.dbname)
            relative_image = os.path.relpath(image, dirname)

            node = ElementTree.SubElement(root, 'Picture')
            node.attrib['id'] = '%s' % p.picture_id
            e = ElementTree.SubElement(node, 'image')
            e.text = '%s' % relative_image
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
        indent(root)
        tree = ElementTree.ElementTree(root)
        d = os.path.dirname(self.dbname)
        tmpname = ''.join([random.choice(string.ascii_letters) for i in range(8)])
        # write out a temporary
        tree.write(os.path.join(d, tmpname), encoding = 'UTF-8')
        # make a backup
        try: os.rename(self.dbname, '%s-bk' % self.dbname)
        except OSError, e: pass
        # move the temporary to the new
        try: os.rename(os.path.join(d, tmpname), self.dbname)
        except OSError, e: pass

    def close(self):
        self._is_open = False
        self._dbname = None
        
        # clear everything
        Agency.clear()
        Calendar.clear()
        Stop.clear()
        Path.clear()
        Route.clear()
        TripRoute.clear()
        Trip.clear()
        Frequency.clear()
        Picture.clear()

    @classmethod
    def export_kml_and_js(cls, directory, messages, calendars_as_placemark = True):
        """Export a self-contained KML file with timetable information,
        and a JSON file with timetable mapping with the names of stops
        and routes as keys. The keys are the same as the 'name' property
        of corresponding placemarks.
        """
        # save the kml
        root = ElementTree.Element('kml')
        root.set('xmlns', '"http://www.opengis.net/kml/2.2"')
        docu = ElementTree.SubElement(root, 'Document')

        # select the icon for bus stops
        e = ElementTree.SubElement(docu, 'Style')
        e.set('id', 'MyBusStop')
        e = ElementTree.SubElement(e, 'IconStyle')
        e = ElementTree.SubElement(e, 'Icon')
        e = ElementTree.SubElement(e, 'href')
        e.text = 'http://maps.google.com/mapfiles/kml/shapes/bus.png'

        # the html content of a blurb with calendars
        cal_table = ElementTree.Element('table')
        node = ElementTree.SubElement(cal_table, 'tr')
        e = ElementTree.SubElement(node, 'th')
        e.text = 'Calendar'
        e = ElementTree.SubElement(node, 'th')
        e.text = 'Monday'
        e = ElementTree.SubElement(node, 'th')
        e.text = 'Tuesday'
        e = ElementTree.SubElement(node, 'th')
        e.text = 'Wednesday'
        e = ElementTree.SubElement(node, 'th')
        e.text = 'Thursday'
        e = ElementTree.SubElement(node, 'th')
        e.text = 'Friday'
        e = ElementTree.SubElement(node, 'th')
        e.text = 'Saturday'
        e = ElementTree.SubElement(node, 'th')
        e.text = 'Sunday'
        e = ElementTree.SubElement(node, 'th')
        e.text = 'Also goes on'
        e = ElementTree.SubElement(node, 'th')
        e.text = 'Does not go on'

        calendars = list(Calendar.calendars)
        calendars.sort(key = lambda c: c.days, reverse = True)
        calendars_js = dict()
        for c in calendars:
            calendars_js[c.name] = {'days': c.days, 'added_excn': c.added_excn, 'remov_excn': c.remov_excn}
        # the calendars
        for c in calendars:
            node = ElementTree.SubElement(cal_table, 'tr')
            e = ElementTree.SubElement(node, 'td')
            e.text = c.name
            for cond in c.days:
                e = ElementTree.SubElement(node, 'td')
                e.text = ('x' if cond == 1 else '-')
                #!lukstafi - TODO: translate dates to nicer format
            e = ElementTree.SubElement(node, 'td')
            e.text = '_'.join(c.added_excn)
            e = ElementTree.SubElement(node, 'td')
            e.text = '_'.join(c.remov_excn)
        calendars = map(lambda c: c.name, calendars)

        cal_table = ElementTree.tostring(cal_table, encoding = 'utf-8', method = 'html')
        if calendars_as_placemark:
            node = ElementTree.SubElement(docu, 'Placemark')
            e = ElementTree.SubElement(node, 'name')
            e.text = 'Days of operation'
            e = ElementTree.SubElement(node, 'Point')
            e = ElementTree.SubElement(e, 'coordinates')
            #!lukstafi - TODO: better location selection
            e.text = '%s,%s' % (Stop.stops[0].longitude,
                                Stop.stops[1].latitude)
            e = ElementTree.SubElement(node, 'description')
            e.text = cal_table
        else:
            node = ElementTree.SubElement(docu, 'description')
            node.text = cal_table
            # no Point element

        # Tabulate the times at stops and on routes.
        # stop->route->calendar->list of departure times
        # route->stop->calendar->list of departure times (transpose of above)
        stop_tables_js = dict()
        route_tables_js = dict()
        for t in Trip.trips:
            for rs in t.stops:
                s_name = rs.stop.code or rs.stop.name or rs.stop.description
                r_name = t.trip_route.route.short_name or t.trip_route.route.long_name or t.trip_route.route.description
                #!lukstafi - FIXME: we need trip route calendar rather than
                # trip calendar, find out why old trip calendars are reset
                c_name = t.trip_route.calendar.name

                if s_name not in stop_tables_js:
                    stop_tables_js[s_name] = dict()
                if r_name not in stop_tables_js[s_name]:
                    stop_tables_js[s_name][r_name] = dict()
                if c_name not in stop_tables_js[s_name][r_name]:
                    stop_tables_js[s_name][r_name][c_name] = list()
                if r_name not in route_tables_js:
                    route_tables_js[r_name] = dict()
                if s_name not in route_tables_js[r_name]:
                    route_tables_js[r_name][s_name] = dict()
                if c_name not in route_tables_js[r_name][s_name]:
                    route_tables_js[r_name][s_name][c_name] = list()
                stop_tables_js[s_name][r_name][c_name].append(rs.departure)
                route_tables_js[r_name][s_name][c_name].append(rs.departure)

        #!lukstafi - TODO: handle the frequencies!

        # the stops
        for s in Stop.stops:
            s_name = s.code or s.name or s.description
            if s_name not in stop_tables_js:
                continue
            node = ElementTree.SubElement(docu, 'Placemark')
            e = ElementTree.SubElement(node, 'name')
            e.text = s_name
            e = ElementTree.SubElement(node, 'styleUrl')
            e.text = '#MyBusStop'
            e = ElementTree.SubElement(node, 'Point')
            e = ElementTree.SubElement(e, 'coordinates')
            e.text = '%s,%s' % (s.longitude, s.latitude)
            stop_tbl = ElementTree.Element('div')
            e = ElementTree.SubElement(stop_tbl, 'span')
            # e = ElementTree.SubElement(stop_tbl, 'b')
            e.text = s.name + ' - ' + s.description
            for r_name, tbl in stop_tables_js[s_name].viewitems():
                tbl_e = ElementTree.SubElement(stop_tbl, 'table')
                # route name
                e = ElementTree.SubElement(tbl_e, 'tr')
                e = ElementTree.SubElement(e, 'th')
                e.text = r_name
                # calendars
                cals = ElementTree.SubElement(tbl_e, 'tr')
                for c_name in calendars:
                    if c_name not in tbl:
                        continue
                    e = ElementTree.SubElement(cals, 'th')
                    e.text = c_name
                cals = ElementTree.SubElement(tbl_e, 'tr')
                for c_name in calendars:
                    if c_name not in tbl:
                        continue
                    e = ElementTree.SubElement(cals, 'td')
                    times_table(e, tbl[c_name])

            e = ElementTree.SubElement(node, 'description')
            #stop_tree = ElementTree.ElementTree(stop_tbl)
            e.text = ElementTree.tostring(stop_tbl, encoding = 'utf-8', method = 'html')

        #!lukstafi - TODO: perhaps split the routes with different
        #   sets of stops into route-calenadar groups
        # route->list of stops on the route
        route_stops = dict()
        for tr in TripRoute.trip_routes:
            if tr.route.route_id in route_stops:
                if len(tr.stops) > len(route_stops[tr.route.route_id]):
                    route_stops[tr.route.route_id] = tr.stops
            else:
                route_stops[tr.route.route_id] = tr.stops

        # the routes
        for r in Route.routes:
            r_name = r.short_name or r.long_name or r.description
            if r_name not in route_tables_js:
                continue
            node = ElementTree.SubElement(docu, 'Placemark')
            e = ElementTree.SubElement(node, 'name')
            e.text = r_name
            e = ElementTree.SubElement(node, 'LineString')
            #!lukstafi - TODO: use user-defined paths when available
            e = ElementTree.SubElement(e, 'coordinates')
            stops = map(lambda s: '%s,%s' % (s.longitude, s.latitude), route_stops[r.route_id])
            e.text = '\n'.join(stops)
            route_h = ElementTree.Element('div')
            e = ElementTree.SubElement(route_h, 'span')
            # e = ElementTree.SubElement(stop_tbl, 'b')
            e.text = r.long_name + ' - ' + r.description
            route_tbl = ElementTree.SubElement(route_h, 'table')
            # stops
            stops_e = ElementTree.SubElement(route_tbl, 'tr')
            for s_name, tbl in route_tables_js[r_name].viewitems():
                e = ElementTree.SubElement(stops_e, 'th')
                e.text = s_name
            stops_e = ElementTree.SubElement(route_tbl, 'tr')
            for s_name, tbl in route_tables_js[r_name].viewitems():
                tbl_e = ElementTree.SubElement(stops_e, 'td')
                tbl_e = ElementTree.SubElement(tbl_e, 'table')
                # calendars
                cals = ElementTree.SubElement(tbl_e, 'tr')
                for c_name in calendars:
                    if c_name not in tbl:
                        continue
                    e = ElementTree.SubElement(cals, 'th')
                    e.text = c_name
                cals = ElementTree.SubElement(tbl_e, 'tr')
                for c_name in calendars:
                    if c_name not in tbl:
                        continue
                    e = ElementTree.SubElement(cals, 'td')
                    times_table(e, tbl[c_name])

            e = ElementTree.SubElement(node, 'description')
            # route_tree = ElementTree.ElementTree(route_tbl)
            e.text = ElementTree.tostring(route_h, encoding = 'utf-8', method = 'html')

        # make a tree and save it
        indent(root)
        tree = ElementTree.ElementTree(root)
        tree.write(os.path.join(directory, 'doc.kml'), encoding = 'UTF-8')

        with open(os.path.join(directory, 'doc.js'), 'w') as outfile:
            outfile.write('var msg1 = "' + messages[0] + '"\n')
            outfile.write('var msg2 = "' + messages[1] + '"\n')
            outfile.write('var msg3 = "' + messages[2] + '"\n')
            outfile.write('var calendars = ')
            json.dump(calendars_js, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
            outfile.write('\nvar stop_tables = ')
            json.dump(stop_tables_js, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
            outfile.write('\nvar route_tables = ')
            json.dump(route_tables_js, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
                           

    @classmethod
    def export(cls, directory, messages):
        Agency.write_agencies(directory)
        Calendar.write_calendars(directory)
        Stop.write_stops(directory)
        Route.write_routes(directory)
        Trip.write_trips(directory)
        Frequency.write_frequencies(directory)
        Path.write_paths(directory)
        cls.export_kml_and_js(directory, messages)

    @classmethod
    def import_gtfs(cls, directory):
        Agency.import_agencies(directory)
        Calendar.import_calendars(directory)
        Stop.import_stops(directory)
        Path.import_paths(directory)
        Route.import_routes(directory)
        Trip.import_trips(directory)
        Frequency.import_frequencies(directory)

def indent(elem, level = 0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def split_time(t):
    if len(t) <= 2: assert False
    if len(t) <= 5:
        pos3 = len(t)
    else:
        if t[4] == ':':
            pos3 = 4
        else:
            if t[5] == ':':
                pos3 = 5
            else:
                pos3 = 4
    if t[1] == ':':
        pos1 = 1
        pos2 = 2
    else:
        if t[2] == ':':
            pos1 = 2
            pos2 = 3
        else:
            if len(t) == 3:
                pos1 = 1
                pos2 = 1
            else:
                pos1 = 2
                pos2 = 2
    return (t[0:pos1], t[pos2:pos3])

def times_table (root, times):
    table = ElementTree.SubElement(root, 'table')
    times = filter(lambda x: x, times)
    times = map(split_time, times)
    for h, minutes in groupby(times, key=(lambda x: x[0])):
        node = ElementTree.SubElement(table, 'tr')
        e = ElementTree.SubElement(node, 'td')
        e = ElementTree.SubElement(e, 'b')
        e.text = h
        for m in minutes:
            e = ElementTree.SubElement(node, 'td')
            e.text = m[1]


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
