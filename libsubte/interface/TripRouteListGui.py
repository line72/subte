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

from gi.repository import Gtk, GObject

import libsubte

class TripRouteListGui(object):
    def __init__(self):
        self.scrolled_window = Gtk.ScrolledWindow(None, None)

        self.model = Gtk.ListStore(GObject.TYPE_INT, str)
        self.treeview = Gtk.TreeView(model = self.model)
        self.treeview.set_rules_hint(True)
        self.treeview.set_headers_visible(True)

        self.clear_model()

        # add the columns to the tree
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Trip Route', renderer, text = 1)
        column.set_sort_column_id(1)
        self.treeview.append_column(column)

        self.scrolled_window.add(self.treeview)

    def get_widget(self):
        return self.scrolled_window

    def get_selected(self):
        '''Returns the selected TripRoute'''
        selection = self.treeview.get_selection()
        if selection is None:
            return None
        store, it = selection.get_selected()
        if store is None or it is None:
            return None

        trip_route_id = store.get_value(it, 0)
        trip_route = libsubte.TripRoute.get(trip_route_id)

        return trip_route

    def set_selected(self, trip_route):
        if not trip_route:
            return

        it = self.model.get_iter_first()
        while it:
            trip_route_id = self.model.get_value(it, 0)

            if trip_route_id == trip_route.trip_route_id:
                self.treeview.set_cursor(self.model.get_path(it))
                return True

            it = self.model.iter_next(it)
        return False

    def clear_model(self):
        self.model.clear()

    def add_trip_route(self, tr):
        if tr:
            name = tr.name
            if tr.route:
                name = '%s - %s' % (tr.route.short_name, tr.name)
            self.model.append([tr.trip_route_id, name])

    def update_trip_route(self, tr):
        if tr:
            # search for this
            it = self.model.get_iter_first()
            while it:
                trip_route_id = self.model.get_value(it, 0)

                if tr.trip_route_id == trip_route_id:
                    name = tr.name
                    if tr.route:
                        name = '%s - %s' % (tr.route.short_name, tr.name)

                    self.model.set_value(it, 1, name)
                    return True

                it = self.model.iter_next(it) 
        return False

    def remove_trip_route(self, tr):
        if tr:
            # search for this
            it = self.model.get_iter_first()
            while it:
                trip_route_id = self.model.get_value(it, 0)

                if tr.trip_route_id == trip_route_id:
                    self.model.remove(it)
                    return True

                it = self.model.iter_next(it)

        return False

    def remove_selection(self):
        selection = self.treeview.get_selection()
        if selection is None:
            return False

        store, it = selection.get_selected()
        if store is None or it is None:
            return False

        self.model.remove(it)

    def get_trip_routes(self):
        trip_routes = []

        it = self.model.get_iter_first()
        while it:
            trip_route_id = self.model.get_value(it, 0)
            trip_route = libsubte.TripRoute.get(trip_route_id)
            trip_routes.append(trip_route)

            it = self.model.iter_next(it)

        return trip_routes
