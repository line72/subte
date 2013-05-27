#!/usr/bin/env python
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

'''
Script to convert older styles save state files
to the new version with trip routes.
'''
import sys
import os

import xml.etree.ElementTree as ElementTree
import xml.parsers.expat

import libsubte

def main():
    try:
        d = os.path.expanduser('~')
        tree = ElementTree.parse(os.path.join(d, '.subte.xml'))

        for agency_node in tree.getroot().findall('Agency'):
            agency_id = agency_node.get('id', libsubte.Agency.new_id())
            name = agency_node.findtext('name')
            url = agency_node.findtext('url')
            timezone = agency_node.findtext('timezone')
            language = agency_node.findtext('language')
            phone = agency_node.findtext('phone')
            fare_url = agency_node.findtext('fare_url')

            a = libsubte.Agency(name = name, url = url, timezone = timezone, language = language,
                       phone = phone, fare_url = fare_url)
            a.agency_id = int(agency_id)

        for calendar_node in tree.getroot().findall('Calendar'):
            calendar_id = calendar_node.get('id', libsubte.Calendar.new_id())
            name = calendar_node.findtext('name')
            days = calendar_node.findtext('days')
            start_date = calendar_node.findtext('start_date')
            end_date = calendar_node.findtext('end_date')

            days = [int(x) for x in days.split()]
            c = libsubte.Calendar(service_name = name, monday = days[0],
                         tuesday = days[1], wednesday = days[2],
                         thursday = days[3], friday = days[4],
                         saturday = days[5], sunday = days[6],
                         start_date = start_date, end_date = end_date)
            c.calendar_id = int(calendar_id)

        for stop_node in tree.getroot().findall('Stop'):
            stop_id = stop_node.get('id', libsubte.Stop.new_id())
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
                s = libsubte.Stop(code = code, name = name, description = description,
                         latitude = float(latitude), longitude = float(longitude),
                         zone_id = zone_id, url = url, location_type = location_type,
                         parent_station = parent_station)
                s.stop_id = int(stop_id)
            except Exception, e:
                print >> sys.stderr, 'Error loading stop', name, e

        for path_node in tree.getroot().findall('Path'):
            path_id = path_node.get('id', libsubte.Path.new_id())
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
                p = libsubte.Path(name = name, coords = coords)
                p.path_id = int(path_id)
            except Exception, e:
                print >> sys.stderr, 'Error loading path', name, e

        for route_node in tree.getroot().findall('Route'):
            route_id = route_node.get('id', libsubte.Route.new_id())
            agency_id = route_node.findtext('agency_id')
            short_name = route_node.findtext('short_name')
            long_name = route_node.findtext('long_name')
            description = route_node.findtext('description')
            route_type = route_node.findtext('route_node')
            url = route_node.findtext('url')
            color = route_node.findtext('color')
            text_color = route_node.findtext('text_color')
            path_id = route_node.findtext('path_id')

            agency_id = int(agency_id)
            r = libsubte.Route(agency = libsubte.Agency.get(agency_id),
                      short_name = short_name, long_name = long_name,
                      description = description, route_type = route_type,
                      url = url, color = color, text_color = text_color)
            r.route_id = int(route_id)

            path = None
            try:
                path = libsubte.Path.get(int(path_id))
                r.set_path(path)
            except Exception, e:
                pass

            # stops
            stops = []
            stops_node = route_node.find('Stops')
            for stop_node in stops_node.findall('Stop'):
                stop_id = stop_node.get('id', None)
                if stop_id is None:
                    print >> sys.stderr, 'Invalid Route stop', stop_id
                else:
                    s = libsubte.Stop.get(int(stop_id))
                    if s:
                        stops.append(s)
                    else:
                        print >> sys.stderr, 'Invalid route stop', stop_id
  
            for calendar in libsubte.Calendar.calendars:
                tr = libsubte.TripRoute('', r, calendar, '', 0, path)
                r.add_trip_route(tr)
                for stop in stops:
                    tr.add_stop(stop)


        for trip_node in tree.getroot().findall('Trip'):
            trip_id = trip_node.get('id', libsubte.Trip.new_id())
            name = trip_node.findtext('name')
            calendar_id = trip_node.findtext('calendar_id')
            route_id = trip_node.findtext('route_id')

            route = libsubte.Route.get(int(route_id))
            calendar = libsubte.Calendar.get(int(calendar_id))

            tr = None
            for trip_route in route.trip_routes:
                if trip_route.calendar == calendar:
                    tr = trip_route
                    break

            trip = tr.add_trip()
            trip.trip_id = int(trip_id)
            trip.name = name

            # trip stops
            trip_stops_node = trip_node.find('TripStops')
            for trip_stop_node in trip_stops_node.findall('TripStop'):
                stop_id = trip_stop_node.findtext('stop_id')
                arrival = trip_stop_node.findtext('arrival')
                departure = trip_stop_node.findtext('departure')

                stop = libsubte.Stop.get(int(stop_id))
                trip_stop = trip.get_stop(stop)

                trip_stop.arrival = arrival
                trip_stop.departure = departure

        for picture_node in tree.getroot().findall('Picture'):
            picture_id = picture_node.get('id', libsubte.Picture.new_id())
            image = picture_node.findtext('image')
            stop_id = picture_node.findtext('stop_id', -1)
            ignored = picture_node.findtext('ignored')
            latitude = picture_node.findtext('latitude')
            longitude = picture_node.findtext('longitude')
            orientation = picture_node.findtext('orientation')

            try:
                stop_id = int(stop_id)
                ignored = bool(int(ignored))

                stop = libsubte.Stop.get(stop_id)

                if latitude is not None and longitude is not None and orientation is not None:
                    p = libsubte.Picture(image, latitude = float(latitude), longitude = float(longitude), orientation = int(orientation))
                else:
                    p = libsubte.Picture(image)

                if stop:
                    stop.add_picture(p)

                p.picture_id = int(picture_id)
            except Exception, e:
                print >> sys.stderr, 'Invalid picture: %s' % e

    except (IOError, xml.parsers.expat.ExpatError), e:
        print 'Error loading saved state', e
        return

    db = libsubte.Database()
    db.save(os.path.join(os.path.expanduser('~'), '.libsubte.db'))


if __name__ == '__main__':
    main()
