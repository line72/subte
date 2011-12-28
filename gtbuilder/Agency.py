
import weakref

from BaseObject import BaseObject

class Agency(BaseObject):
    agencies = []

    def __init__(self, agency_id = None, name = None, url = None,
                 timezone = 'America/Chicago', language = 'en', phone = None, fare_url = None):
        BaseObject.__init__(self)

        self.agency_id = agency_id
        self.name = name
        self.url = url
        self.timezone = timezone
        self.language = language
        self.phone = phone
        self.fare_url = fare_url

        # add us
        Agency.agencies.append(weakref.ref(self))

    def write(self, f):
        self._write(f, '%s,%s,%s,%s,%s,%s,%s\n', 
                    self.agency_id, self.name or '',
                    self.url or '', self.timezone,
                    self.language, self.phone or '', 
                    self.fare_url or '')
        
    @classmethod
    def write_agencies(cls):
        f = open('agency.txt', 'w')
        # header
        f.write('agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone,agency_fare_url\n')
        for a in cls.agencies:
            if a():
                a().write(f)
        f.close()

if __name__ == '__main__':
    a1 = Agency('bjcta', 'Birmingham-Jefferson County Transit Authority',
                url = 'http://www.bjcta.org', fare_url = 'http://www.bjcta.org/fares/fare_structure.cfm')

    Agency.write_agencies()
