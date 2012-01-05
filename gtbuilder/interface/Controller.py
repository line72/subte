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

import random
import weakref


import gtbuilder

from AddStop import AddStopDialog, AddStop

class Controller(object):
    '''This is a controller class. It handles all the callbacks
    from the GUI'''
    def __init__(self, gui):
        self._gui = weakref.ref(gui)

    def initialize(self):
        # fill in the initial data
        # stops first
        for s in gtbuilder.Stop.select():
            self.gui.map_widget.add_stop(s)
            self.gui.stop_list_widget.add_stop(s)

        # now routes

    def on_map_click(self, view, event):
        x, y = event.get_coords()
        latitude = view.y_to_latitude(y)
        longitude = view.x_to_longitude(x)
        
        # add a new stop
        #stop = gtbuilder.Stop(name = 'Stop%d' % random.randint(0, 100),
        #                      latitude = latitude, longitude = longitude)

        #self.map_widget.add_stop(stop)
        #self.stop_list_widget.add_stop(stop)

        for i in self._registered_events.get('on-map-clicked', []):
            i(view, event)

        return True

    def on_stop_list_selected(self, treeview, user_data = None):
        selection = treeview.get_selection()
        store, it = selection.get_selected()

        stop_id = store.get_value(it, 0)
        stop = gtbuilder.Stop.get(stop_id)

        return True

    def on_add_stop(self, toolbutton, user_data = None):
        print 'adding a stop'
        stop_dialog = AddStop(self)

        win = AddStopDialog()
        win.get_content_area().add(stop_dialog)
        win.show_all()

        resp = win.run()
        win.destroy()
        print 'resp=', resp

    gui = property(lambda x: x._gui(), None)
