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

import weakref
import sys

from gi.repository import Gtk

import libsubte

from StopListGui import StopListGui
from AgencyDialog import AgencyChoice
from PathDialog import PathChoice

class AddRouteDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, 'Add Route', parent,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            ('Add', Gtk.ResponseType.ACCEPT,
                            'Cancel', Gtk.ResponseType.CANCEL))
class EditRouteDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, 'Edit Route', parent,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            ('Edit', Gtk.ResponseType.ACCEPT,
                            'Cancel', Gtk.ResponseType.CANCEL))

class AddRoute(Gtk.VBox):
    '''A dialog that creates a new route'''
    def __init__(self, controller, route = None):
        Gtk.VBox.__init__(self, False)
        
        self._controller = weakref.ref(controller)

        size_group = Gtk.SizeGroup(mode = Gtk.SizeGroupMode.HORIZONTAL)

        # name
        hbox = Gtk.HBox(False)
        name_lbl = Gtk.Label('Short Name: ')
        size_group.add_widget(name_lbl)       
        hbox.pack_start(name_lbl, False, False, 0)
        self.name_txt = Gtk.Entry()
        hbox.pack_start(self.name_txt, True, True, 5)

        self.pack_start(hbox, True, False, 5)

        # name
        hbox = Gtk.HBox(False)
        name_lbl = Gtk.Label('Long Name: ')
        size_group.add_widget(name_lbl)       
        hbox.pack_start(name_lbl, False, False, 0)
        self.long_name_txt = Gtk.Entry()
        hbox.pack_start(self.long_name_txt, True, True, 5)

        self.pack_start(hbox, True, False, 5)


        # description
        hbox = Gtk.HBox(False)
        description_lbl = Gtk.Label('Description: ')
        size_group.add_widget(description_lbl)       
        hbox.pack_start(description_lbl, False, False, 0)
        self.description_txt = Gtk.TextView()
        hbox.pack_start(self.description_txt, True, True, 5)

        self.pack_start(hbox, True, True, 5)

        # agency
        self.agency_hbox = AgencyChoice()
        size_group.add_widget(self.agency_hbox.get_label())
        self.pack_start(self.agency_hbox, True, False, 5)

        # path
        self.path_hbox = PathChoice()
        size_group.add_widget(self.path_hbox.get_label())
        self.pack_start(self.path_hbox, True, False, 5)

        # stop list
        hbox = Gtk.HBox(False)
        stop_lbl = Gtk.Label('Stops: ')
        size_group.add_widget(stop_lbl)
        hbox.pack_start(stop_lbl, False, False, 0)
        self.stop_list = StopListGui()
        hbox.pack_start(self.stop_list.get_widget(), True, True, 5)
        # actions
        vbox = Gtk.VBox(True)
        add_btn = Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
        rm_btn = Gtk.Button.new_from_stock(Gtk.STOCK_REMOVE)
        up_btn = Gtk.Button.new_from_stock(Gtk.STOCK_GO_UP)
        down_btn = Gtk.Button.new_from_stock(Gtk.STOCK_GO_DOWN)

        rm_btn.connect('clicked', self.on_remove_stop)
        up_btn.connect('clicked', self.on_raise_stop)
        down_btn.connect('clicked', self.on_lower_stop)

        vbox.pack_start(add_btn, False, False, 5)
        vbox.pack_start(rm_btn, False, False, 5)
        vbox.pack_start(up_btn, False, False, 5)
        vbox.pack_start(down_btn, False, False, 5)
        hbox.pack_start(vbox, False, False, 0)

        self.pack_start(hbox, True, True, 5)

        self._fill(route)

    def get_name(self):
        return self.name_txt.get_text()

    def get_long_name(self):
        return self.long_name_txt.get_text()

    def get_description(self):
        b = self.description_txt.get_buffer()
        return b.get_text(b.get_start_iter(), b.get_end_iter(), False)

    def set_description(self, desc):
        b = Gtk.TextBuffer()
        b.set_text(desc)
        self.description_txt.set_buffer(b)

    def get_agency(self):
        return self.agency_hbox.get_selection()

    def get_path(self):
        return self.path_hbox.get_selection()

    def get_stops(self):
        return self.stop_list.get_stops()

    def on_stop_selected(self, stop):
        print 'on_stop_selected', stop
        # !mwd - are duplicate stops ok?
        #  We may use the same stops just in
        #  a different direction.
        # !mwd - I really don't think we
        #  should allow duplicates, it 
        #  breaks things. We should have
        #  two stops, one going each direction
        self.stop_list.add_stop(stop)

        return True

    def on_remove_stop(self, btn, user_data = None):
        self.stop_list.remove_selection()

        return True

    def on_raise_stop(self, btn, user_data = None):
        self.stop_list.raise_selection()

        return True

    def on_lower_stop(self, btn, user_data = None):
        self.stop_list.lower_selection()

        return True

    def _fill(self, route):
        if route is None:
            return

        self.name_txt.set_text(route.short_name)
        self.long_name_txt.set_text(route.long_name)
        self.set_description(route.description)
        self.agency_hbox.set_selection(route.agency.name)
        if route.path:
            self.path_hbox.set_selection(route.path.name)

        # fill the stops
        for s in route.stops:
            self.stop_list.add_stop(s)
