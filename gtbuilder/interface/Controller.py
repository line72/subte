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

import gtbuilder

class Controller(object):
    '''This is a controller class. It handles all the callbacks
    from the GUI'''
    def __init__(self, map_widget, stop_list_widget):
        self.map_widget = map_widget
        self.stop_list_widget = stop_list_widget

        # signals
        self.map_widget.view.connect('button-release-event', self.on_map_click)
        self.stop_list_widget.treeview.connect('cursor-changed', self.on_stop_list_selected)

        # fill in the initial data
        # stops first
        for s in gtbuilder.Stop.select():
            self.map_widget.add_stop(s)
            self.stop_list_widget.add_stop(s)

        # now routes

    def on_map_click(self, view, event):
        x, y = event.get_coords()
        latitude = view.y_to_latitude(y)
        longitude = view.x_to_longitude(x)
        
        # add a new stop
        stop = gtbuilder.Stop(name = 'Stop%d' % random.randint(0, 100),
                              latitude = latitude, longitude = longitude)

        self.map_widget.add_stop(stop)
        self.stop_list_widget.add_stop(stop)

        return True

    def on_stop_list_selected(self, treeview, user_data = None):
        selection = treeview.get_selection()
        store, it = selection.get_selected()

        stop_id = store.get_value(it, 0)
        stop = gtbuilder.Stop.get(stop_id)


        return True
