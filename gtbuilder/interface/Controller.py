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

from gi.repository import Gtk

import gtbuilder

from AddStop import AddStopDialog, AddStop

class Controller(object):
    '''This is a controller class. It handles all the callbacks
    from the GUI'''
    class SignalHandler(object):
        def __init__(self, fn, args):
            self._fn = fn
            self._args = args

    def __init__(self, gui):
        self._gui = weakref.ref(gui)
        self._registered_events = {}

    def initialize(self):
        # fill in the initial data
        # stops first
        for s in gtbuilder.Stop.select():
            self.gui.map_widget.add_stop(s)
            self.gui.stop_list_widget.add_stop(s)

        # now routes

    def connect(self, signal, fn, *args):
        if signal not in self._registered_events:
            self._registered_events[signal] = []

        handler = Controller.SignalHandler(fn, args)
        self._registered_events[signal].append(handler)

        return handler

    def disconnect(self, signal, handler):
        try:
            self._registered_events[signal].remove(handler)
        except Exception:
            pass

    def on_map_click(self, view, event):
        x, y = event.get_coords()
        latitude = view.y_to_latitude(y)
        longitude = view.x_to_longitude(x)
        
        # add a new stop
        #stop = gtbuilder.Stop(name = 'Stop%d' % random.randint(0, 100),
        #                      latitude = latitude, longitude = longitude)

        #self.map_widget.add_stop(stop)
        #self.stop_list_widget.add_stop(stop)

        for handler in self._registered_events.get('on-map-clicked', []):
            handler._fn(view, event, *(handler._args))

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

        win = AddStopDialog(self._gui())
        win.get_content_area().add(stop_dialog)
        win.show_all()

        handler = self.connect('on-map-clicked', stop_dialog.on_map_clicked)

        resp = win.run()
        print 'resp=', resp
        self.disconnect('on-map-clicked', handler)

        if resp == Gtk.ResponseType.ACCEPT:
            # create a new stop
            s = gtbuilder.Stop(name = stop_dialog.get_name(),
                               description = stop_dialog.get_description(),
                               latitude = stop_dialog.get_latitude(),
                               longitude = stop_dialog.get_longitude())
            
            self.gui.map_widget.add_stop(s)
            self.gui.stop_list_widget.add_stop(s)


        win.destroy()

    gui = property(lambda x: x._gui(), None)
