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
from RouteListGui import RouteListGui

class GTGui(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = 'Google Transit Builder')
        self.connect('delete-event', self.on_quit)

        # load up our database
        self.db = gtbuilder.Database(os.path.join(os.path.expanduser('~'), '.gtbuilder.db'))

        #!mwd - temp
        #agency = gtbuilder.Agency(name = 'BJCTA')

        # setup a controller
        self.controller = Controller(self)

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
        notebook = Gtk.Notebook()
        box.pack_start(notebook, True, True, 5)

        self.stop_list_widget = StopListGui()
        notebook.append_page(self.stop_list_widget.get_widget(), Gtk.Label('Stops'))
        self.route_list_widget = RouteListGui()
        notebook.append_page(self.route_list_widget.get_widget(), Gtk.Label('Routes'))

        self.info_frame.add(box)

        # map frame
        box = Gtk.VBox(False)
        self.map_widget = GTMap()        
        box.pack_start(self.map_widget, True, True, 5)
        self.map_frame.add(box)

        vbox.pack_start(self.main_pane, True, True, 15)

        self.add(vbox)

        # initialize the controller
        self.controller.initialize()
        
        # some signals
        self.map_widget.view.connect('button-release-event', self.controller.on_map_click)
        self.stop_list_widget.treeview.connect('cursor-changed', self.controller.on_stop_list_selected)
        self.route_list_widget.treeview.connect('cursor-changed', self.controller.on_route_list_selected)


    def on_quit(self, widget, evt, data = None):
        Gtk.main_quit()

    def _build_tool_bar(self):
        toolbar = Gtk.Toolbar()
        toolbar.set_icon_size(Gtk.IconSize.LARGE_TOOLBAR)
        #toolbar.set_style(Gtk.ToolbarStyle.BOTH_HORIZ)

        ## STOPS
        #!mwd - how do I add a frakin' label?
        #stop_lbl = Gtk.ToolButton()
        #stop_lbl.set_label('Stops:')
        #stop_lbl.set_label_widget(Gtk.Label('Stops:'))
        #toolbar.add(stop_lbl)

        add_stop = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ADD)
        add_stop.set_tooltip_text('Add a new stop')
        add_stop.connect('clicked', self.controller.on_add_stop_clicked)
        toolbar.add(add_stop)

        remove_stop = Gtk.ToolButton.new_from_stock(Gtk.STOCK_REMOVE)
        remove_stop.set_tooltip_text('Remove a stop')
        remove_stop.connect('clicked', self.controller.on_remove_stop_clicked)
        toolbar.add(remove_stop)

        toolbar.add(Gtk.SeparatorToolItem())

        ## ROUTES
        add_route = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ADD)
        add_route.set_tooltip_text('Add a new route')
        add_route.connect('clicked', self.controller.on_add_route_clicked)
        toolbar.add(add_route)

        remove_route = Gtk.ToolButton.new_from_stock(Gtk.STOCK_REMOVE)
        remove_route.set_tooltip_text('Remove a route')
        remove_route.connect('clicked', self.controller.on_remove_route_clicked)
        toolbar.add(remove_route)

        toolbar.add(Gtk.SeparatorToolItem())

        return toolbar
