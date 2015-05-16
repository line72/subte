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
from Locale import _

from CalendarDialog import CalendarChoice

class TripListDialog(Gtk.Dialog):
    def __init__(self, parent, trip_route):
        Gtk.Dialog.__init__(self, _('Edit Trips'), parent,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            (_('Close'), Gtk.ResponseType.CLOSE,))

        self.get_content_area().pack_start(TripList(trip_route), True, True, 5)

class TripList(Gtk.VBox):
    def __init__(self, trip_route):
        Gtk.VBox.__init__(self, False)

        self._trip_route = trip_route

        # trip editor
        trip_hbox = Gtk.HBox(False)
        self.pack_start(trip_hbox, True, True, 5)

        self.scrolled_window = Gtk.ScrolledWindow(None, None)

        # add a final column for the next trip
        cols = [GObject.TYPE_INT, str]
        self.next_block_model = Gtk.ListStore(*cols)
        self.next_block_model.append((-1, ''))
        print 'TripList: trip_route.route',trip_route.route
        if trip_route.route:
            for i in trip_route.route.trip_routes:
                if i == self:
                    continue
                if i.calendar == trip_route.calendar:
                    direction = _('Outbound') if i.direction == 0 else _('Inbound')
                    for j in i.trips:
                        if len(j.stops) > 0:
                            self.next_block_model.append((j.trip_id, '%s @ %s' % (direction, j.stops[0].arrival)))
        else:
            assert False

        cols = [GObject.TYPE_INT]
        for i in trip_route.stops:
            cols.append(str)
        cols.append(str)

        self.model = Gtk.ListStore(*cols)
        self.treeview = Gtk.TreeView(model = self.model)
        self.treeview.set_rules_hint(True)
        self.treeview.set_headers_visible(True)

        self.clear_model()

        # add the columns
        cp = 1
        for c, i in enumerate(trip_route.stops):
            renderer = Gtk.CellRendererText()
            renderer.props.editable = True
            renderer.connect('edited', self.on_cell_edited, c+1)
            #!mwd - text is the column in the list store where
            #  we get our text from. Since our first column (id)
            #  is hidden, it is c+1
            column = Gtk.TreeViewColumn(i.name, renderer, text = c+1)
            self.treeview.append_column(column)
            cp = c + 2
        # and a column for the next block
        combo_renderer = Gtk.CellRendererCombo()
        combo_renderer.set_property("editable", "False")
        combo_renderer.set_property("model", self.next_block_model)
        combo_renderer.set_property("text-column", 1)
        combo_renderer.set_property("has-entry", False)
        #combo_renderer.connect("edited", self.on_next_block_edited)
        combo_renderer.connect("changed", self.on_next_block_changed)
        column = Gtk.TreeViewColumn(_("Next Trip"), combo_renderer, text = cp)
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
        rm_button = Gtk.Button.new_from_stock(Gtk.STOCK_REMOVE)
        rm_button.connect('clicked', self.on_rm_trip)
        vbox.pack_start(rm_button, False, False, 0)
        trip_hbox.pack_start(vbox, False, False, 5)

    def update_model(self):
        # update the model to show the trips based on the 
        #  current calendar
        self.clear_model()

        # add the trips that use this calendar
        for i, t in enumerate(self._trip_route.trips):
            trip = [t.trip_id]
            for j, s in enumerate(self._trip_route.stops):
                ts = t.stops[j]
                trip.append(ts.arrival)

            # see if there is a next block
            if t.next_block:
                it = self.next_block_model.get_iter_first()
                done = False
                while it and not done:
                    cols = [0, 1]
                    values = self.next_block_model.get(it, *cols)

                    if values[0] == t.next_block.trip_id:
                        trip.append(values[1])
                        done = True

                    it = self.next_block_model.iter_next(it)

                if not done:
                    print 'Unable to find a match for the next stop. This must be a missing reference'
                    trip.append('') # didn't find a match
            else:
                trip.append('')

            self.model.append(trip)

    def clear_model(self):
        self.model.clear()

    def add_trip(self, t):
        trip = [t.trip_id]
        for i, s in enumerate(self._trip_route.stops):
            ts = t.stops[i]
            trip.append(ts.arrival)

        # see if there is a next block
        if t.next_block:
            it = self.next_block_model.get_iter_first()
            done = False
            while it and not done:
                cols = [0, 1]
                values = self.next_block_model.get(it, *cols)

                if values[0] == t.next_block.trip_id:
                    trip.append(values[1])
                    done = True

                it = self.next_block_model.iter_next(it)

            if not done:
                print 'Unable to find a match for the next stop. This must be a missing reference'
                trip.append('') # didn't find a match
        else:
            trip.append('')


        self.model.append(trip)

    def on_add_trip(self, btn, user_data = None):
        #trip_name = '%s%d' % (self._trip_route.route.short_name, len(self._trip_route.trips))
        t = self._trip_route.add_trip()
        self.add_trip(t)

        return True

    def on_rm_trip(self, btn, user_data = None):
        selection = self.treeview.get_selection()
        if selection is None:
            return True

        store, it = selection.get_selected()
        if store is None or it is None:
            return True
        
        trip_id = self.model.get(it, 0)[0]

        trip = libsubte.Trip.get(trip_id)
        if trip:
            self._trip_route.remove_trip(trip)
            trip.destroy()

        self.model.remove(it)

        return True

    def on_cell_edited(self, renderer, path, text, column):
        # !mwd - validate

        # update the gtk model
        it = self.model.get_iter_from_string(path)
        self.model.set_value(it, column, text)

        # update our model
        trips = self._trip_route.trips
        try:
            trip = trips[int(path)]
            stop = self._trip_route.stops[column-1]
            #trip_stop = trip.get_stop(stop)
            trip_stop = trip.stops[column-1]
            trip_stop.arrival = text
            trip_stop.departure = text
        except (AttributeError, IndexError), e:
            print 'Warning->', e
            return False

        return True

    def on_next_block_edited(self, widget, path, text):
        self.model[path][len(self._trip_route.stops) + 1] = text

        print 'widget=', widget

        # look up the id in the next_block_model
        it = self.next_block_model.get_iter_first();
        while it:
            cols = [0, 1]
            values = self.next_block_model.get(it, *cols)
            print 'values = ', values

            it = self.next_block_model.iter_next(it)

        return True

    def on_next_block_changed(self, widget, path, it):
        # get the value
        cols = [0, 1]
        values = self.next_block_model.get(it, *cols)

        # set the text
        self.model[path][len(self._trip_route.stops) + 1] = values[1]

        # try to look up the next Trip
        next_trip = libsubte.Trip.get(values[0])
        
        # get our current trip
        current_trip = self._trip_route.trips[int(path)]

        # set it
        print 'setting next trip for', current_trip, 'to', next_trip
        current_trip.next_block = next_trip

        return True
