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
from AddRoute import AddRouteDialog, AddRoute

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
            self.add_stop(s)
        # now routes
        for r in gtbuilder.Route.select():
            self.add_route(r)

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
        for handler in self._registered_events.get('on-map-clicked', []):
            handler._fn(view, event, *(handler._args))

        return True

    def on_stop_marker_clicked(self, actor, event, stop):
        actor.set_selected(True)

        if stop:
            for handler in self._registered_events.get('on-stop-selected', []):
                handler._fn(stop, *(handler._args))

        return True

    def on_stop_list_selected(self, treeview, user_data = None):
        s = self.gui.stop_list_widget.get_selected()

        # hi-light it?

        return True

    def on_route_list_selected(self, treeview, user_data = None):
        r = self.gui.route_list_widget.get_selected()

        self.gui.map_widget.draw_route(r)

        return True

    def on_add_stop_clicked(self, toolbutton, user_data = None):
        print 'adding a stop'
        stop_dialog = AddStop(self)

        win = AddStopDialog(self._gui())
        win.get_content_area().add(stop_dialog)
        win.show_all()

        handler = self.connect('on-map-clicked', stop_dialog.on_map_clicked)

        resp = win.run()
        self.disconnect('on-map-clicked', handler)

        if resp == Gtk.ResponseType.ACCEPT:
            # create a new stop
            s = gtbuilder.Stop(name = stop_dialog.get_name(),
                               description = stop_dialog.get_description(),
                               latitude = stop_dialog.get_latitude(),
                               longitude = stop_dialog.get_longitude())
            
            self.add_stop(s)

        win.destroy()

    def on_remove_stop_clicked(self, toolbutton, user_data = None):
        print 'removing stop'
        stop = self.gui.stop_list_widget.get_selected()
        if stop is None:
            print 'Nothing selected'
            return

        # remove this from our widgets
        self.gui.map_widget.remove_stop(stop)
        self.gui.stop_list_widget.remove_stop(stop)

        # good-bye
        stop.destroySelf()

    def on_add_route_clicked(self, toolbutton, user_data = None):
        print 'on add route'
        route_dialog = AddRoute(self)

        win = AddRouteDialog(self._gui())
        win.get_content_area().add(route_dialog)
        win.show_all()

        handler = self.connect('on-stop-selected', route_dialog.on_stop_selected)

        resp = win.run()
        self.disconnect('on-stop-selected', handler)

        if resp == Gtk.ResponseType.ACCEPT:
            # create a new route
            default_agency = gtbuilder.Agency.get(1)
            r = gtbuilder.Route(agency = default_agency, 
                                short_name = route_dialog.get_name(),
                                description = route_dialog.get_description())
            for s in route_dialog.get_stops():
                r.addStop(s)

            self.add_route(r)
            
        win.destroy()

    def on_remove_route_clicked(self, toolbutton, user_data = None):
        print 'on remove route'
        route = self.gui.route_list_wiget.get_selected()
        if route is None:
            print 'Nothing selected'
            return

        # remove this from our widgets
        self.gui.map_widget.remove_route(route)
        self.gui.route_list_widget.remove_route(route)

        # good-bye
        route.destroySelf()

    def add_stop(self, s):
        m = self.gui.map_widget.add_stop(s)
        m.connect('button-release-event', self.on_stop_marker_clicked, s)
        self.gui.stop_list_widget.add_stop(s)

    def add_route(self, r):
        path = self.gui.map_widget.draw_route(r)
        # connect a signal
        
        self.gui.route_list_widget.add_route(r)

    gui = property(lambda x: x._gui(), None)
