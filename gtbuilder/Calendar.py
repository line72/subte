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

import sqlobject

class Calendar(sqlobject.SQLObject):
    name = sqlobject.StringCol()
    monday = sqlobject.BoolCol(default = False)
    tuesday = sqlobject.BoolCol(default = False)
    wednesday = sqlobject.BoolCol(default = False)
    thursday = sqlobject.BoolCol(default = False)
    friday = sqlobject.BoolCol(default = False)
    saturday = sqlobject.BoolCol(default = False)
    sunday = sqlobject.BoolCol(default = False)
    start = sqlobject.DateCol()
    end = sqlobject.DateCol()
    trips = sqlobject.RelatedJoin('Trip')

# import weakref

# from datetime import datetime
# from dateutil.relativedelta import relativedelta

# from BaseObject import BaseObject

# class Calendar(BaseObject):
#     calendars = []

#     def __init__(self, service_id, monday = 0,
#                  tuesday = 0, wednesday = 0, thursday = 0,
#                  friday = 0, saturday = 0, sunday = 0,
#                  start_date = None, end_date = None):
#         BaseObject.__init__(self)

#         self.service_id = service_id
#         self.days = [monday, tuesday, wednesday,
#                      thursday, friday, saturday,
#                      sunday]
#         #self.start_date = start_date or datetime.now()
#         #self.end_date = end_date or datetime.now() + relativedelta(years=+1)
#         self.start_date = start_date
#         self.end_date = end_date

#         # add us
#         Calendar.calendars.append(weakref.ref(self))

#     def write(self, f):
#         self._write(f, '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n',
#                     self.service_id,
#                     self.days[0], self.days[1], self.days[2],
#                     self.days[3], self.days[4], self.days[5], self.days[6],
#                     self.start_date,
#                     self.end_date)

#     @classmethod
#     def write_calendars(cls):
#         f = open('calendar.txt', 'w')
#         # header
#         f.write('service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n')
#         for c in cls.calendars:
#             if c():
#                 c().write(f)
#         f.close()

#     @classmethod
#     def get_calendar(cls, service_id):
#         for c in cls.calendars:
#             if c() and c().service_id == service_id:
#                 return c()
#         return None
