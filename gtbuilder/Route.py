
import weakref

from BaseObject import BaseObject
from Trip import Trip
from Stop import Stop

class Route(BaseObject):
    routes = []

    def __init__(self, route_id, agency, short_name = '',
                 long_name = '', description = '',
                 route_type = None, url = '', color = None, text_color = None):
        BaseObject.__init__(self)

        self.route_id = route_id
        self.agency = agency
        self.short_name = short_name
        self.long_name = long_name
        self.description = description
        self.route_type = route_type
        self.url = url
        self.color = color
        self.text_color = text_color

        self.trips = []

        # add us
        Route.routes.append(weakref.ref(self))

    def add_trip(self, name, calendar):
        trip = Trip(name, self, calendar)
        self.trips.append(trip)
    
        return trip

    def build_trips(self, csv, calendar, trip_name = None):
        '''build trips from a csv file.'''
        f = open(csv)
        stops = f.readline().strip().split(',')

        if trip_name is None:
            trip_name = csv[:-4] # remove the .csv

        for i, l in enumerate(f.readlines()):
            trip = self.add_trip('%s%d' % (trip_name, i), calendar)
            
            times = l.strip().split(',')

            previous_stop = ''
            for s, t in zip(stops, times):
                if t == '--': # skip
                    continue
                if s == previous_stop:
                    # set the departure time
                    trip.stops[-1].departure = t
                else:
                    # a blank time is ok, it just means
                    #  google will interpolate it
                    trip.add_stop(Stop.get_stop(s), t)
                
                previous_stop = s


    def write(self, f):
        self._write(f, '%s,%s,%s,%s,%s,%s,%s,%s,%s\n',
                    self.route_id, self.agency.agency_id,
                    self.short_name or '', self.long_name or '',
                    self.description or '', self.route_type or 3,
                    self.url or '', self.color or '',
                    self.text_color or '')

    @classmethod
    def write_routes(cls):
        f = open('routes.txt', 'w')
        # header
        f.write('route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color\n')
        for r in cls.routes:
            if r():
                r().write(f)
        f.close()


