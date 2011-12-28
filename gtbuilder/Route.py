
import weakref

from BaseObject import BaseObject
from Trip import Trip

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


