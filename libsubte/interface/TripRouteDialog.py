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

from gi.repository import Gtk
import weakref

import libsubte

from CalendarDialog import CalendarChoice
from PathDialog import PathChoice
from RouteDialog import RouteChoice
from StopListGui import StopListGui
from TripList import TripListDialog
from FrequencyList import FrequencyListDialog

class AddTripRouteDialog(Gtk.Dialog):
    def __init__(self, parent, trip_route):
        Gtk.Dialog.__init__(self, 'Add Trip', parent,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            ('Add', Gtk.ResponseType.ACCEPT,
                             'Cancel', Gtk.ResponseType.CANCEL))

        self.content = AddTripRoute(trip_route)
        self.get_content_area().add(self.content)
        self.set_modal(False)

class EditTripRouteDialog(Gtk.Dialog):
    def __init__(self, parent, trip_route):
        Gtk.Dialog.__init__(self, 'Edit Trip', parent,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            ('Edit', Gtk.ResponseType.ACCEPT,))

        self.content = AddTripRoute(trip_route)
        self.get_content_area().add(self.content)
        self.set_modal(False)


class AddTripRoute(Gtk.VBox):
    '''A vbox for adding a single trip along a route'''
    def __init__(self, trip_route):
        Gtk.VBox.__init__(self, False)

        self._trip_route = trip_route

        size_group = Gtk.SizeGroup(mode = Gtk.SizeGroupMode.HORIZONTAL)

        # name
        hbox = Gtk.HBox(False)
        name_lbl = Gtk.Label('Name: ')
        size_group.add_widget(name_lbl)       
        hbox.pack_start(name_lbl, False, False, 0)
        self.name_txt = Gtk.Entry()
        hbox.pack_start(self.name_txt, True, True, 5)
        self.pack_start(hbox, True, True, 5)

        # route
        self.route_hbox = RouteChoice()
        size_group.add_widget(self.route_hbox.get_label())
        self.pack_start(self.route_hbox, True, False, 5)

        # calendar
        self.calendar_hbox = CalendarChoice()
        size_group.add_widget(self.calendar_hbox.get_label())
        self.pack_start(self.calendar_hbox, True, False, 5)

        # path
        self.path_hbox = PathChoice()
        size_group.add_widget(self.path_hbox.get_label())
        self.pack_start(self.path_hbox, True, False, 5)

        # headsign
        hbox = Gtk.HBox(False)
        headsign_lbl = Gtk.Label('Headsign: ')
        size_group.add_widget(headsign_lbl)       
        hbox.pack_start(headsign_lbl, False, False, 0)
        self.headsign_txt = Gtk.Entry()
        hbox.pack_start(self.headsign_txt, True, True, 5)
        self.pack_start(hbox, True, True, 5)

        # direction
        hbox = Gtk.HBox(False)
        direction_lbl = Gtk.Label('Direction: ')
        size_group.add_widget(direction_lbl)
        hbox.pack_start(direction_lbl, False, False, 0)
        self.direction = Gtk.ComboBoxText.new()
        hbox.pack_start(self.direction, True, True, 5)
        self.pack_start(hbox, True, True, 5)

        self.direction.append_text('Outbound')
        self.direction.append_text('Inbound')
        self.direction.set_active(0)

        # edit trips
        hbox = Gtk.HBox(False)
        edit_trips_lbl = Gtk.Label('Edit Trips: ')
        size_group.add_widget(edit_trips_lbl)
        hbox.pack_start(edit_trips_lbl, False, False, 0)
        edit_trip_btn = Gtk.Button.new_from_stock(Gtk.STOCK_INFO)
        edit_trip_btn.connect('clicked', self.on_modify_trips)
        hbox.pack_start(edit_trip_btn, True, True, 5)
        self.pack_start(hbox, True, True, 5)

        # edit frequencies
        hbox = Gtk.HBox(False)
        edit_frequencies_lbl = Gtk.Label('Edit Frequencies: ')
        size_group.add_widget(edit_frequencies_lbl)
        hbox.pack_start(edit_frequencies_lbl, False, False, 0)
        edit_frequencies_btn = Gtk.Button.new_from_stock(Gtk.STOCK_INFO)
        edit_frequencies_btn.connect('clicked', self.on_modify_frequencies)
        hbox.pack_start(edit_frequencies_btn, True, True, 5)
        self.pack_start(hbox, True, True, 5)

        # and all our stops
        hbox = Gtk.HBox(False)
        stops_lbl = Gtk.Label('Stops: ')
        size_group.add_widget(stops_lbl)
        hbox.pack_start(stops_lbl, False, False, 0)
        self.stops = StopListGui()
        hbox.pack_start(self.stops.get_widget(), True, True, 5)
        # actions
        vbox = Gtk.VBox(True)
        #add_btn = Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
        rm_btn = Gtk.Button.new_from_stock(Gtk.STOCK_REMOVE)
        up_btn = Gtk.Button.new_from_stock(Gtk.STOCK_GO_UP)
        down_btn = Gtk.Button.new_from_stock(Gtk.STOCK_GO_DOWN)

        #add_btn.connect('clicked', self.on_move_stop_left)
        rm_btn.connect('clicked', self.on_remove_stop)
        up_btn.connect('clicked', self.on_raise_stop)
        down_btn.connect('clicked', self.on_lower_stop)

        #vbox.pack_start(add_btn, False, False, 5)
        vbox.pack_start(rm_btn, False, False, 5)
        vbox.pack_start(up_btn, False, False, 5)
        vbox.pack_start(down_btn, False, False, 5)
        hbox.pack_start(vbox, False, True, 0)

        self.pack_start(hbox, True, True, 5)
        
        self.fill()

    def fill(self):
        if self._trip_route is None:
            return

        self.name_txt.set_text(self._trip_route.name)
        self.route_hbox.set_selection(self._trip_route.route)
        self.calendar_hbox.set_selection(self._trip_route.calendar)
        self.path_hbox.set_selection(self._trip_route.path)
        self.headsign_txt.set_text(self._trip_route.headsign)
        self.direction.set_active(self._trip_route.direction)

        # stops
        for stop in self._trip_route.stops:
            self.stops.add_stop(stop)

    def get_name(self):
        return self.name_txt.get_text()

    def get_route(self):
        return self.route_hbox.get_selection()

    def get_calendar(self):
        return self.calendar_hbox.get_selection()

    def get_headsign(self):
        return self.headsign_txt.get_text()

    def get_direction(self):
        selection = self.direction.get_active_text()
        if selection == 'Outbound':
            return 0
        return 1 # inbound

    def get_path(self):
        return self.path_hbox.get_selection()

    def get_stops(self):
        return self.stops.get_stops()

    def on_stop_selected(self, stop):
        print 'on_stop_selected TripRoute',stop
        self.stops.add_stop(stop)
        self._trip_route.add_stop(stop)

        return True

    def on_remove_stop(self, btn):
        index = self.stops.get_selected_index()
        self.stops.remove_selection()
        self._trip_route.remove_stop_at(index)

        return True

    def on_raise_stop(self, btn):
        index = self.stops.get_selected_index()
        self.stops.raise_selection()
        self._trip_route.increment_stop_at(index)

        return True

    def on_lower_stop(self, btn):
        index = self.stops.get_selected_index()
        self.stops.lower_selection()
        self._trip_route.decrement_stop_at(index)

        return True
    
    def on_modify_trips(self, btn):
        print 'on-modify-trips'
        if self._trip_route:
            if not self._trip_route.route:
                print 'on-modify-trips: hack - set route',self.get_route()
                self._trip_route.route = self.get_route()
            if not self._trip_route.calendar:
                print 'on-modify-trips: hack - set calendar',self.get_calendar()
                self._trip_route.calendar = self.get_calendar()

            dlg = TripListDialog(None, self._trip_route)
            dlg.show_all()

            dlg.run()

            dlg.destroy()

        return True
    
    def on_modify_frequencies(self, btn):
        if self._trip_route:
            dlg = FrequencyListDialog(None, self._trip_route)
            dlg.show_all()

            dlg.run()

            dlg.destroy()

        return True
