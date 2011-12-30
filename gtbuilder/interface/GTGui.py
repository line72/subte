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

import string
import random

from gi.repository import Gtk

from GTMap import GTMap
#from GTServer import GTServer

class GTGui(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = 'Google Transit Builder')
        self.connect('delete-event', self.on_quit)

        # generate a key (32-long)
        #self.__key = ''.join(random.choice(string.letters + string.digits) for x in range(32))

        # spawn off our webserver in a new thread
        #self.__server = GTServer()

        self.gtmap = GTMap()
        self.add(self.gtmap)
        
    def on_quit(self, widget, evt, data = None):
        #self.__server.stop()
        Gtk.main_quit()

