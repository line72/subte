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

import string
import random
import os

from gi.repository import Gtk

import gtbuilder

from GTMap import GTMap
from Controller import Controller
from StopListGui import StopListGui

class GTGui(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = 'Google Transit Builder')
        self.connect('delete-event', self.on_quit)

        # load up our database
        self.db = gtbuilder.Database(os.path.join(os.path.expanduser('~'), '.gtbuilder.db'))

        vbox = Gtk.VBox(False)

        # a tool bar
        toolbar = self._build_tool_bar()
        vbox.pack_start(toolbar, False, True, 0)

        # a horizontal pane
        self.main_pane = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        self.info_frame = Gtk.Frame()
        self.map_frame = Gtk.Frame()

        self.main_pane.pack1(self.info_frame)
        self.main_pane.pack2(self.map_frame)

        # info frame
        box = Gtk.VBox(False)
        combo_box = Gtk.ComboBoxText.new()
        combo_box.append_text('Stops')
        combo_box.append_text('Routes')
        combo_box.set_active(0) # set the first to active
        combo_box.connect('changed', self.on_combo_changed)
        box.pack_start(combo_box, False, True, 5)

        self.stop_tree = StopListGui()
        box.pack_start(self.stop_tree.get_widget(), True, True, 5)

        self.info_frame.add(box)

        # map frame
        box = Gtk.VBox(False)
        self.gtmap = GTMap()
        box.pack_start(self.gtmap, True, True, 5)
        self.map_frame.add(box)

        vbox.pack_start(self.main_pane, True, True, 15)

        self.add(vbox)
        
        # setup a controller
        self.controller = Controller(map_widget = self.gtmap,
                                     stop_list_widget = self.stop_tree)

    def on_quit(self, widget, evt, data = None):
        Gtk.main_quit()

    def on_combo_changed(self, widget, data = None):
        txt = widget.get_active_text()

        return True

    def _build_tool_bar(self):
        toolbar = Gtk.Toolbar()

        add_stop = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ADD)
        toolbar.insert(add_stop, 0)

        toolbar.insert(Gtk.SeparatorToolItem(), 1)

        toolbar.set_icon_size(Gtk.IconSize.LARGE_TOOLBAR)

        return toolbar
