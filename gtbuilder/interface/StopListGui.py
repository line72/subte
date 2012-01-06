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

class StopListGui(object):
    def __init__(self):
        self.model = Gtk.ListStore(GObject.TYPE_INT, str)
        self.treeview = Gtk.TreeView(model = self.model)
        self.treeview.set_rules_hint(True)
        self.treeview.set_headers_visible(False)
       
        self.clear_model()
 
        # add the columns to the tree
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Stop', renderer, text = 1)
        column.set_sort_column_id(0)
        self.treeview.append_column(column)

    def get_widget(self):
        return self.treeview

    def get_selected(self):
        '''Returns the selected Stop'''
        selection = self.treeview.get_selection()
        if selection is None:
            return None
        store, it = selection.get_selected()
        if store is None or it is None:
            return None

        stop_id = store.get_value(it, 0)
        stop = gtbuilder.Stop.get(stop_id)

        return stop

    def clear_model(self):
        # clear the old model
        self.model.clear()

    def add_stop(self, s):
        print 'add_stop', s
        if s:
            name = s.name
            if name is None:
                name = s.id
            print 'appending'
            self.model.append([s.id, '(%s) %s' % (s.id, name)])

    def remove_stop(self, s):
        if s:
            # search for this
            pass

    def get_stops(self):
        stops = []

        it = self.model.get_iter_first()
        while it:
            stop_id = self.model.get_value(it, 0)
            stop = gtbuilder.Stop.get(stop_id)
            stops.append(stop)

            it = self.model.iter_next(it)

        return stops
