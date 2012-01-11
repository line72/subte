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

import gtbuilder

class RouteListGui(object):
    def __init__(self):
        self.scrolled_window = Gtk.ScrolledWindow(None, None)

        self.model = Gtk.ListStore(GObject.TYPE_INT, str)
        self.treeview = Gtk.TreeView(model = self.model)
        self.treeview.set_rules_hint(True)
        self.treeview.set_headers_visible(False)
       
        self.clear_model()
 
        # add the columns to the tree
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Route', renderer, text = 1)
        column.set_sort_column_id(0)
        self.treeview.append_column(column)

        self.scrolled_window.add(self.treeview)

    def get_widget(self):
        return self.scrolled_window

    def get_selected(self):
        '''Returns the selected Route'''
        selection = self.treeview.get_selection()
        if selection is None:
            return None
        store, it = selection.get_selected()
        if store is None or it is None:
            return None

        route_id = store.get_value(it, 0)
        route = gtbuilder.Route.get(route_id)

        return route

    def clear_model(self):
        # clear the old model
        self.model.clear()

    def add_route(self, s):
        print 'add_route', s
        if s:
            name = s.short_name
            if name is None:
                name = s.route_id
            print 'appending'
            self.model.append([s.route_id, '(%s) %s' % (s.route_id, name)])

    def remove_route(self, route):
        if route:
            # search for this
            it = self.model.get_iter_first()
            while it:
                route_id = self.model.get_value(it, 0)
                r = gtbuilder.Route.get(route_id)

                if r == route:
                    print 'match'
                    self.model.remove(it)
                    return True

                it = self.model.iter_next(it)

        return False

    def get_routes(self):
        routes = []

        it = self.model.get_iter_first()
        while it:
            route_id = self.model.get_value(it, 0)
            route = gtbuilder.Route.get(route_id)
            routes.append(route)

            it = self.model.iter_next(it)

        return routes
