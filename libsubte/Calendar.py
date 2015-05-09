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
import csv

from BaseObject import BaseObject
from libsubte import TripRoute
from libsubte import Trip

class Calendar(BaseObject):
    calendars = []
    calendar_id = 0

    def __init__(self, service_name,
                 monday = 1, tuesday = 1, wednesday = 1, thursday = 1,
                 friday = 1, saturday = 1, sunday = 1,
                 start_date = '20150601', end_date = '20170601',
                 added_excn = [], remov_excn = []):
        BaseObject.__init__(self)

        self.calendar_id = Calendar.new_id()
        self.name = service_name
        self.days = [monday, tuesday, wednesday,
                     thursday, friday, saturday,
                     sunday]
        self.start_date = start_date
        self.end_date = end_date
        self.added_excn = added_excn
        self.remov_excn = remov_excn

        # add us
        Calendar.calendars.append(self)

    def get_id(self):
        if self.gtfs_id:
            return self.gtfs_id
        return self.calendar_id

    def write(self, f_cal, f_cal_dates):
        self._write(f_cal, '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n',
                    self.get_id(),
                    self.days[0], self.days[1], self.days[2],
                    self.days[3], self.days[4], self.days[5], self.days[6],
                    self.start_date, self.end_date)

        for d in self.added_excn:
            self._write(f_cal_dates, '%s,%s,1\n', self.get_id(), d)
        for d in self.remov_excn:
            self._write(f_cal_dates, '%s,%s,2\n', self.get_id(), d)

    def destroy(self):
        try:
            Calendar.calendars.remove(self)
        except ValueError:
            pass

    @classmethod
    def clear(cls):
        cls.calendars = []
        cls.calendar_id = 0

    @classmethod
    def write_calendars(cls, directory = '.'):
        f_cal = open(os.path.join(directory, 'calendar.txt'), 'w')
        f_cal_dates = open(os.path.join(directory, 'calendar_dates.txt'), 'w')
        # header
        f_cal.write('service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n')
        f_cal_dates.write('service_id,date,exception_type\n')
        for c in cls.calendars:
            c.write(f_cal, f_cal_dates)
        f_cal.close()
        f_cal_dates.close()

    @classmethod
    def get(cls, calendar_id):
        for c in cls.calendars:
            if c.calendar_id == calendar_id:
                return c
        return None

    @classmethod
    def get_by_gtfs_id(cls, gtfs_id):
        for c in cls.calendars:
            if c.gtfs_id == gtfs_id:
                return c
        return None

    @classmethod
    def new_id(cls):
        while True:
            cls.calendar_id += 1
            if cls.calendar_id not in [x.calendar_id for x in Calendar.calendars]:
                return cls.calendar_id

    @classmethod
    def import_calendars(cls, directory):
        try:
            f = open(os.path.join(directory, 'calendar.txt'), 'rb')
            reader = csv.reader(f)

            mappings = {'service_id': 'service_name',
                        'monday': 'monday',
                        'tuesday': 'tuesday',
                        'wednesday': 'wednesday',
                        'thursday': 'thursday',
                        'friday': 'friday',
                        'saturday': 'saturday',
                        'sunday': 'sunday',
                        'start_date': 'start_date',
                        'end_date': 'end_date',
                    }
            transforms = {'service_id': lambda x: x,
                          'monday': lambda x: int(x),
                          'tuesday': lambda x: int(x),
                          'wednesday': lambda x: int(x),
                          'thursday': lambda x: int(x),
                          'friday': lambda x: int(x),
                          'saturday': lambda x: int(x),
                          'sunday': lambda x: int(x),
                          'start_date': lambda x: x,
                          'end_date': lambda x: x,
                      }

            # create a headers with an index
            headers = reader.next()
            r_headers = dict([(x, i) for i, x in enumerate(headers)])

            for l2 in reader:
                if len(l2) != len(headers):
                    print >> sys.stderr, 'Invalid line', l2, headers
                    continue
                
                kw = {}
                for i, a in enumerate(l2):
                    key = headers[i]
                    if key in mappings:
                        kw[mappings[key]] = transforms[key](BaseObject.unquote(a))
                # create the calendar
                calendar = Calendar(**kw)
                # set the id
                calendar.gtfs_id = BaseObject.unquote(l2[r_headers['service_id']])

        except IOError, e:
            print >> sys.stderr, 'Unable to open calendar.txt:', e
