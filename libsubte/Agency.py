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
from BaseObject import BaseObject

class Agency(BaseObject):
    agencies = []
    agency_id = 0

    def __init__(self, name = None, url = None,
                 timezone = 'America/Chicago', language = 'en', phone = None, fare_url = None):
        BaseObject.__init__(self)

        self.agency_id = Agency.new_id()
        self.name = name
        self.url = url
        self.timezone = timezone
        self.language = language
        self.phone = phone
        self.fare_url = fare_url

        # add us
        Agency.agencies.append(self)

    def write(self, f):
        self._write(f, '%s,%s,%s,%s,%s,%s,%s\n', 
                    self.agency_id, self.name or '',
                    self.url or '', self.timezone,
                    self.language, self.phone or '', 
                    self.fare_url or '')

    @classmethod
    def get(cls, agency_id):
        for agency in cls.agencies:
            if agency.agency_id == agency_id:
                return agency
        return None        

    @classmethod
    def clear(cls):
        cls.agencies = []
        cls.agency_id = 0

    @classmethod
    def new_id(cls):
        while True:
            cls.agency_id += 1
            if cls.agency_id not in [x.agency_id for x in Agency.agencies]:
                return cls.agency_id


    @classmethod
    def write_agencies(cls, directory = '.'):
        f = open(os.path.join(directory, 'agency.txt'), 'w')
        # header
        f.write('agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone,agency_fare_url\n')
        for a in cls.agencies:
            a.write(f)
        f.close()

    @classmethod
    def import_agencies(cls, directory):
        try:
            f = open(os.path.join(directory, 'agency.txt'), 'r')

            mappings = {'agency_name': 'name',
                        'agency_url': 'url',
                        'agency_timezone': 'timezone',
                        'agency_lang': 'language',
                        'agency_phone': 'phone',
                        'agency_fare_url': 'fare_url'}

            header_l = f.readline()
            # create a headers with an index
            headers = header_l.strip().split(',')
            r_headers = dict([(x, i) for i, x in enumerate(headers)])

            for l in f.readlines():
                l2 = l.strip().split(',')
                if len(l2) != len(headers):
                    print >> sys.stderr, 'Invalid line', l, l2, headers
                    continue
                
                kw = {}
                for i, a in enumerate(l2):
                    key = headers[i]
                    if key in mappings:
                        kw[mappings[key]] = BaseObject.unquote(a)
                # create the agency
                agency = Agency(**kw)
                # set the id
                agency.agency_id = BaseObject.unquote(l2[r_headers['agency_id']])

        except IOError, e:
            print >> sys.stderr, 'Unable to open agency.txt:', e

if __name__ == '__main__':
    a1 = Agency('bjcta', 'Birmingham-Jefferson County Transit Authority',
                url = 'http://www.bjcta.org', fare_url = 'http://www.bjcta.org/fares/fare_structure.cfm')

    Agency.write_agencies()
