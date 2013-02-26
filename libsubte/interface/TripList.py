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

from CalendarDialog import CalendarChoice

class TripListDialog(Gtk.Dialog):
    def __init__(self, parent, route):
        Gtk.Dialog.__init__(self, 'Edit Trips', parent,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            ('Close', Gtk.ResponseType.CLOSE,))

        self.get_content_area().pack_start(TripList(route), True, True, 5)

class TripList(Gtk.VBox):
    def __init__(self, route):
        Gtk.VBox.__init__(self, False)

        self._route = route

        # calendar editor
        self.calendar_hbox = CalendarChoice()
        self.calendar_hbox.choice.connect('changed', self.on_calendar_changed)
        self.pack_start(self.calendar_hbox, False, False, 5)

        # trip editor
        trip_hbox = Gtk.HBox(False)
        self.pack_start(trip_hbox, True, True, 5)

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
        self.update_model()

        self.scrolled_window.add(self.treeview)

        trip_hbox.pack_start(self.scrolled_window, True, True, 5)

        # create an add button
        vbox = Gtk.VBox(False)
        add_button = Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
        add_button.connect('clicked', self.on_add_trip)
        vbox.pack_start(add_button, False, False, 0)
        trip_hbox.pack_start(vbox, False, False, 5)

    def update_model(self):
        # update the model to show the trips based on the 
        #  current calendar
        self.clear_model()

        calendar = self.get_calendar()

        # add the trips that use this calendar
        for i, t in enumerate(self._route.get_trips_with_calendar(calendar)):
            trip = [i]
            for s in self._route.stops:
                ts = t.get_stop(s)
                trip.append(ts.arrival)
            self.model.append(trip)

    def clear_model(self):
        self.model.clear()

    def get_calendar(self):
        return self.calendar_hbox.get_selection()

    def add_trip(self, t):
        trip = [len(self._route.trips)]
        for s in self._route.stops:
            ts = t.get_stop(s)
            trip.append(ts.arrival)

        self.model.append(trip)

    def on_calendar_changed(self, widget, user_data = None):
        self.update_model()

    def on_add_trip(self, btn, user_data = None):
        if self.get_calendar() is None:
            return

        trip_name = '%s%d' % (self._route.short_name, len(self._route.trips))
        t = self._route.add_trip(trip_name, self.get_calendar())
        self.add_trip(t)

        return True

    def on_cell_edited(self, renderer, path, text, column):
        # !mwd - validate

        # update the gtk model
        it = self.model.get_iter_from_string(path)
        self.model.set_value(it, column, text)

        # update our model
        trips = self._route.get_trips_with_calendar(self.get_calendar())
        try:
            trip = trips[int(path)]
            stop = self._route.stops[column-1]
            trip_stop = trip.get_stop(stop)
            trip_stop.arrival = text
            trip_stop.departure = text
        except (AttributeError, IndexError), e:
            print 'Warning->', e
            return False

        return True
