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

class FrequencyListDialog(Gtk.Dialog):
    def __init__(self, parent, trip_route):
        Gtk.Dialog.__init__(self, 'Edit Frequencies', parent,
                           Gtk.DialogFlags.DESTROY_WITH_PARENT,
                           ('Close', Gtk.ResponseType.CLOSE,))

        self.content = FrequencyList(trip_route)
        self.get_content_area().pack_start(self.content, True, True, 5)

class FrequencyList(Gtk.VBox):
    def __init__(self, trip_route):
        Gtk.VBox.__init__(self, False)

        self._trip_route = trip_route
        
        frequency_hbox = Gtk.HBox(False)
        self.pack_start(frequency_hbox, True, True, 5)

        self.scrolled_window = Gtk.ScrolledWindow(None, None)

        cols = [GObject.TYPE_INT, str, str, str]

        self.model = Gtk.ListStore(*cols)
        self.treeview = Gtk.TreeView(model = self.model)
        self.treeview.set_rules_hint(True)
        self.treeview.set_headers_visible(True)

        self.clear_model()

        # add the columns
        for c, i in enumerate(('Start Time', 'End Time', 'Headway')):
            renderer = Gtk.CellRendererText()
            renderer.props.editable = True
            renderer.connect('edited', self.on_cell_edited, c+1)
            #!mwd - text is the column in the list store where
            #  we get our text from. Since our first column (id)
            #  is hidden, it is c+1
            column = Gtk.TreeViewColumn(i, renderer, text = c+1)
            self.treeview.append_column(column)

        # add the frequencies
        self.update_model()

        self.scrolled_window.add(self.treeview)

        frequency_hbox.pack_start(self.scrolled_window, True, True, 5)

        # create an add button
        vbox = Gtk.VBox(False)
        add_button = Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
        add_button.connect('clicked', self.on_add_frequency)
        vbox.pack_start(add_button, False, False, 0)
        rm_button = Gtk.Button.new_from_stock(Gtk.STOCK_REMOVE)
        rm_button.connect('clicked', self.on_rm_frequency)
        vbox.pack_start(rm_button, False, False, 0)
        frequency_hbox.pack_start(vbox, False, False, 5)

    def update_model(self):
        self.clear_model()

        # add the frequencies that use this calendar
        for i, t in enumerate(self._trip_route.frequencies):
            self.model.append((t.frequency_id, t.start, t.end, t.headway))

    def clear_model(self):
        self.model.clear()

    def add_frequency(self, frequency):
        self.model.append((frequency.frequency_id, frequency.start, frequency.end, frequency.headway))

    def on_add_frequency(self, btn, user_data = None):
        frequency = self._trip_route.add_frequency('', '', '')
        self.add_frequency(frequency)

        return True

    def on_rm_frequency(self, btn, user_data = None):
        selection = self.treeview.get_selection()
        if selection is None:
            return True

        store, it = selection.get_selected()
        if store is None or it is None:
            return True
        
        frequency_id = self.model.get(it, 0)[0]

        frequency = libsubte.Frequency.get(frequency_id)
        if frequency:
            self._trip_route.remove_frequency(frequency)
            frequency.destroy()

        self.model.remove(it)

        return True


    def on_cell_edited(self, renderer, path, text, column):
        # !mwd - validate

        # update the gtk model
        it = self.model.get_iter_from_string(path)
        self.model.set_value(it, column, text)

        frequency_id = self.model.get(it, 0)[0]

        frequency = libsubte.Frequency.get(frequency_id)
        if frequency:
            if column == 1: # start
                frequency.start = text
            elif column == 2: # end 
                frequency.end = text
            elif column == 3: # headway
                frequency.headway = text

        return True
