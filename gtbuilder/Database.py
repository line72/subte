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

import os
import sqlobject

from Route import Route
from Stop import Stop
from Trip import Trip, TripStop
from Calendar import Calendar
from Agency import Agency

class Database(object):
    def __init__(self, fname):
        db_name = os.path.abspath(fname)

        needs_create = False
        try:
            os.stat(db_name)
        except OSError, e:
            needs_create = True

        connection_string = 'sqlite:' + db_name
        
        self._connection = sqlobject.connectionForURI(connection_string)
        sqlobject.sqlhub.processConnection = self._connection

        if needs_create:
            self._create()

    def _create(self):
        Route.createTable()
        Stop.createTable()
        Trip.createTable()
        TripStop.createTable()
        Calendar.createTable()
        Agency.createTable()
