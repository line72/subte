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

from gi.repository import Gtk

import libsubte

class MergeStopsDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, 'Merge Stops', parent, 
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            ('Merge', Gtk.ResponseType.ACCEPT,
                             'Cancel', Gtk.ResponseType.CANCEL))

class MergeStops(Gtk.VBox):
    '''A dialog that merges two stops'''
    def __init__(self, controller):
        Gtk.VBox.__init__(self, False)

        self._stop1 = None
        self._stop2 = None

        self._stop1_selection_active = False
        self._stop2_selection_active = False

        self._controller = weakref.ref(controller)

        size_group = Gtk.SizeGroup(mode = Gtk.SizeGroupMode.HORIZONTAL)

        # stop 1
        hbox = Gtk.HBox(False)
        stop1_lbl = Gtk.Label('Stop 1: ')
        size_group.add_widget(stop1_lbl)
        hbox.pack_start(stop1_lbl, False, False, 0)
        self.stop1_input = Gtk.Label('')
        hbox.pack_start(self.stop1_input, True, False, 0)
        stop1_btn = Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
        stop1_btn.connect('clicked', self.on_stop1_clicked)
        hbox.pack_start(stop1_btn, False, False, 0)

        self.pack_start(hbox, True, True, 5)

        # stop 2
        hbox = Gtk.HBox(False)
        stop2_lbl = Gtk.Label('Stop 2: ')
        size_group.add_widget(stop2_lbl)
        hbox.pack_start(stop2_lbl, False, False, 0)
        self.stop2_input = Gtk.Label('')
        hbox.pack_start(self.stop2_input, True, False, 0)
        stop2_btn = Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
        stop2_btn.connect('clicked', self.on_stop2_clicked)
        hbox.pack_start(stop2_btn, False, False, 0)

        self.pack_start(hbox, True, True, 5)

    @property
    def stop1(self):
        return self._stop1
    @property
    def stop2(self):
        return self._stop2

    def on_stop1_clicked(self, widget, data = None):
        self._stop1_selection_active = True
        return True

    def on_stop2_clicked(self, widget, data = None):
        self._stop2_selection_active = True
        return True

    def on_stop_selected(self, stop):
        name = stop.name
        if name is None:
            name = stop.stop_id

        if self._stop1_selection_active:
            self.stop1_input.set_text(name)
            self._stop1 = stop
            self._stop1_selection_active = False
        elif self._stop2_selection_active:
            self.stop2_input.set_text(name)
            self._stop2 = stop
            self._stop2_selection_active = False

        return True
