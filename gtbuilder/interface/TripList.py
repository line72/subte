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

class TripListDialog(Gtk.Dialog):
    def __init__(self, parent, route):
        Gtk.Dialog.__init__(self, 'Edit Trips', parent,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            ('Close', Gtk.ResponseType.CLOSE,))

        self.get_content_area().add(TripList(route))

class TripList(Gtk.HBox):
    def __init__(self, route):
        Gtk.HBox.__init__(self, False)

        self._route = route

        self.scrolled_window = Gtk.ScrolledWindow(None, None)

        cols = [GObject.TYPE_INT]
        for i in route.stops:
            cols.append(str)

        self.model = Gtk.ListStore(*cols)
        self.treeview = Gtk.TreeView(model = self.model)
        self.treeview.set_rules_hint(True)
        self.treeview.set_headers_visible(True)

        self.clear_model()

        # add the columns
        for c, i in enumerate(route.stops):
            renderer = Gtk.CellRendererText()
            renderer.props.editable = True
            renderer.connect('edited', self.on_cell_edited, c+1)
            #!mwd - text is the column in the list store where
            #  we get our text from. Since our first column (id)
            #  is hidden, it is c+1
            column = Gtk.TreeViewColumn(i.name, renderer, text = c+1)
            self.treeview.append_column(column)

        # add the trips
        for i, t in enumerate(route.trips):
            trip = [i]
            for s in self._route.stops:
                ts = t.get_stop(s)
                trip.append(ts.arrival)
            self.model.append(trip)

        self.scrolled_window.add(self.treeview)

        self.pack_start(self.scrolled_window, True, True, 5)

        # create an add button
        add_button = Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
        add_button.connect('clicked', self.on_add_trip)
        self.pack_start(add_button, False, False, 5)

    def clear_model(self):
        self.model.clear()

    def add_trip(self, t):
        trip = [len(self._route.trips)]
        for s in self._route.stops:
            ts = t.get_stop(s)
            trip.append(ts.arrival)

        self.model.append(trip)

    def on_add_trip(self, btn, user_data = None):
        t = self._route.add_trip('trip0', gtbuilder.Calendar.get(1))
        self.add_trip(t)

        return True

    def on_cell_edited(self, renderer, path, text, column):
        # !mwd - validate

        # update the gtk model
        it = self.model.get_iter_from_string(path)
        self.model.set_value(it, column, text)

        # update our model
        try:
            trip = self._route.trips[int(path)]
            stop = self._route.stops[column-1]
            trip_stop = trip.get_stop(stop)
            trip_stop.arrival = text
        except (AttributeError, IndexError), e:
            print 'Warning->', e
            return False

        return True
