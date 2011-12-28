
import weakref

from datetime import datetime
from dateutil.relativedelta import relativedelta

from BaseObject import BaseObject

class Calendar(BaseObject):
    calendars = []

    def __init__(self, service_id, monday = 0,
                 tuesday = 0, wednesday = 0, thursday = 0,
                 friday = 0, saturday = 0, sunday = 0,
                 start_date = None, end_date = None):
        BaseObject.__init__(self)

        self.service_id = service_id
        self.days = [monday, tuesday, wednesday,
                     thursday, friday, saturday,
                     sunday]
        #self.start_date = start_date or datetime.now()
        #self.end_date = end_date or datetime.now() + relativedelta(years=+1)
        self.start_date = start_date
        self.end_date = end_date

        # add us
        Calendar.calendars.append(weakref.ref(self))

    def write(self, f):
        self._write(f, '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n',
                    self.service_id,
                    self.days[0], self.days[1], self.days[2],
                    self.days[3], self.days[4], self.days[5], self.days[6],
                    self.start_date,
                    self.end_date)

    @classmethod
    def write_calendars(cls):
        f = open('calendar.txt', 'w')
        # header
        f.write('service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n')
        for c in cls.calendars:
            if c():
                c().write(f)
        f.close()
