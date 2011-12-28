
import weakref

from BaseObject import BaseObject

class Stop(BaseObject):
    stops = []

    def __init__(self, stop_id = None, code = None, name = None,
                 description = None, latitude = None, longitude = None,
                 zone_id = None, url = None, location_type = 0, parent_station = None):
        BaseObject.__init__(self)

        self.stop_id = stop_id
        self.code = code
        self.name = name
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self.zone_id = zone_id
        self.url = url
        self.location_type = location_type
        self.parent_station = parent_station

        # add us
        Stop.stops.append(weakref.ref(self))

    def write(self, f):
        self._write(f, '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n',
                    self.stop_id, self.code,
                    self.name, self.description,
                    self.latitude, self.longitude,
                    self.zone_id, self.url,
                    self.location_type or 0,
                    self.parent_station)

    @classmethod
    def get_stop(cls, stop_id):
        for s in cls.stops:
            if s():
                if s().stop_id == stop_id:
                    return s()
        return None
        
    @classmethod
    def write_stops(cls):
        f = open('stops.txt', 'w')
        # header
        f.write('stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,location_type,parent_station\n')
        for s in cls.stops:
            if s():
                s().write(f)
        f.close()

if __name__ == '__main__':
    s1 = Stop('central', '', 'Central Station', '',
              33.511878, -86.808826, 'zone1', '', 0, '')
    s2 = Stop('summit', '', 'Summit', 'Summit Shopping Center',
              33.44800, -86.73103, 'zone1', '', 0, '')

    s1 = None

    Stop.write_stops()
