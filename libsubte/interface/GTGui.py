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
import sys
import weakref

from gi.repository import Gtk, Gio

import libsubte
from Locale import _

from GTMap import GTMap
from Controller import Controller
from StopListGui import StopListGui
from RouteListGui import RouteListGui
from TripRouteListGui import TripRouteListGui
from PathListGui import PathListGui

class GTGui(Gtk.Window):
    instance = None
    def __init__(self):
        Gtk.Window.__init__(self, title = 'Subte GTFS Builder', type = Gtk.WindowType.TOPLEVEL)
        self.set_icon_name('subte')

        GTGui.instance = weakref.ref(self)

        self.connect('delete-event', self.on_quit)

        # load up our database
        self.db = libsubte.Database()

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
        notebook.append_page(self.stop_list_widget.get_widget(), Gtk.Label(_('Stops')))
        self.trip_list_widget = TripRouteListGui()
        notebook.append_page(self.trip_list_widget.get_widget(), Gtk.Label(_('Trips')))
        self.path_list_widget = PathListGui()
        notebook.append_page(self.path_list_widget.get_widget(), Gtk.Label(_('Paths')))

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
        #!lukstafi -- changed button-release to button-press
        self.map_widget.view.connect('button-press-event', self.controller.on_map_click, self.map_widget)
        #!lukstafi -- for some reason AddTripRoute dialogs behave as modal
        # although they should be modeless, and these or similar signals
        # are not sent when AddTripRoute dialogs are open
        self.stop_list_widget.treeview.connect('cursor-changed', self.controller.on_stop_list_selected)
        self.trip_list_widget.treeview.connect('cursor-changed', self.controller.on_route_trip_list_selected)

    def on_quit(self, widget, evt, data = None):
        # try to save
        if self.controller.clear_project(True) == False: # they cancelled, stay in
            return True

        GTGui.instance = None
        Gtk.main_quit()

        return True
        
    def _build_tool_bar(self):
        toolbar = Gtk.Toolbar()
        toolbar.set_icon_size(Gtk.IconSize.LARGE_TOOLBAR)
        #toolbar.set_style(Gtk.ToolbarStyle.BOTH_HORIZ)

        ## LOAD/SAVE/CLOSE DB
        load_db = Gtk.ToolButton.new_from_stock(Gtk.STOCK_OPEN)
        load_db.set_tooltip_text(_('Load a project'))
        load_db.connect('clicked', self.controller.on_load_project_clicked)
        toolbar.add(load_db)
        
        save_db = Gtk.ToolButton.new_from_stock(Gtk.STOCK_SAVE)
        save_db.set_tooltip_text(_('Save a project'))
        save_db.connect('clicked', self.controller.on_save_project_clicked)
        toolbar.add(save_db)
        
        close_db = Gtk.ToolButton.new_from_stock(Gtk.STOCK_CLOSE)
        close_db.set_tooltip_text(_('Close a project'))
        close_db.connect('clicked', self.controller.on_close_project_clicked)
        toolbar.add(close_db)

        toolbar.add(Gtk.SeparatorToolItem())

        ## STOPS
        #!mwd - how do I add a frakin' label?
        #stop_lbl = Gtk.ToolButton()
        #stop_lbl.set_label('Stops:')
        #stop_lbl.set_label_widget(Gtk.Label('Stops:'))
        #toolbar.add(stop_lbl)

        add_stop = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ADD)
        add_stop.set_tooltip_text(_('Add a new stop'))
        add_stop.connect('clicked', self.controller.on_add_stop_clicked)
        toolbar.add(add_stop)

        edit_stop = Gtk.ToolButton.new_from_stock(Gtk.STOCK_EDIT)
        edit_stop.set_tooltip_text(_('Edit a new stop'))
        edit_stop.connect('clicked', self.controller.on_edit_stop_clicked)
        toolbar.add(edit_stop)

        remove_stop = Gtk.ToolButton.new_from_stock(Gtk.STOCK_REMOVE)
        remove_stop.set_tooltip_text(_('Remove a stop'))
        remove_stop.connect('clicked', self.controller.on_remove_stop_clicked)
        toolbar.add(remove_stop)

        merge_stop = Gtk.ToolButton()
        merge_stop.set_icon_name('gtk-copy')
        merge_stop.set_tooltip_text(_('Merge two stops'))
        merge_stop.connect('clicked', self.controller.on_merge_stops_clicked)
        toolbar.add(merge_stop)

        toolbar.add(Gtk.SeparatorToolItem())

        ## TRIPS
        add_trip = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ADD)
        add_trip.set_tooltip_text(_('Add a new trip'))
        add_trip.connect('clicked', self.controller.on_add_trip_clicked)
        toolbar.add(add_trip)

        edit_trip = Gtk.ToolButton.new_from_stock(Gtk.STOCK_EDIT)
        edit_trip.set_tooltip_text(_('Edit a trip'))
        edit_trip.connect('clicked', self.controller.on_edit_trip_clicked)
        toolbar.add(edit_trip)

        remove_trip = Gtk.ToolButton.new_from_stock(Gtk.STOCK_REMOVE)
        remove_trip.set_tooltip_text(_('Remove a trip'))
        remove_trip.connect('clicked', self.controller.on_remove_trip_clicked)
        toolbar.add(remove_trip)

        copy_trip = Gtk.ToolButton()
        copy_trip.set_icon_name('gtk-copy')
        copy_trip.set_tooltip_text(_('Copy a trip'))
        copy_trip.connect('clicked', self.controller.on_copy_trip_clicked)
        toolbar.add(copy_trip)

        toolbar.add(Gtk.SeparatorToolItem())

        ## PICTURES
        add_picture = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ADD)
        add_picture.set_tooltip_text(_('Add a new picture'))
        add_picture.connect('clicked', self.controller.on_add_picture_clicked)
        toolbar.add(add_picture)
        
        # remove_picture = Gtk.ToolButton.new_from_stock(Gtk.STOCK_REMOVE)
        # remove_picture.set_tooltip_text('Remove a picture')
        # remove_picture.connect('clicked', self.controller.on_remove_picture_clicked)
        # toolbar.add(remove_picture)
        
        toolbar.add(Gtk.SeparatorToolItem())


        ## PATHS
        add_path = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ADD)
        add_path.set_tooltip_text(_('Add a new path from a .kml (or .kmz) file'))
        add_path.connect('clicked', self.controller.on_add_path_clicked)
        toolbar.add(add_path)

        remove_path = Gtk.ToolButton.new_from_stock(Gtk.STOCK_REMOVE)
        remove_path.set_tooltip_text(_('Remove a path'))
        remove_path.connect('clicked', self.controller.on_remove_path_clicked)
        toolbar.add(remove_path)

        toolbar.add(Gtk.SeparatorToolItem())

        ## Import
        import_gtfs = Gtk.ToolButton('Import')
        import_gtfs.set_icon_name('document-import')
        import_gtfs.set_tooltip_text(_('Import GTFS'))
        import_gtfs.connect('clicked', self.controller.on_import_gtfs)
        toolbar.add(import_gtfs)

        ## EXPORT
        export = Gtk.ToolButton('Export')
        export.set_icon_name('document-send')
        export.set_tooltip_text(_('Export to GTFS'))
        export.connect('clicked', self.controller.on_export_gtfs)
        toolbar.add(export)

        export = Gtk.ToolButton('Export')
        export.set_icon_name('document-send')
        export.set_tooltip_text(_('Export to KML by agencies'))
        export.connect('clicked', self.controller.on_export_kml_agencies)
        toolbar.add(export)

        export = Gtk.ToolButton('Export')
        export.set_icon_name('document-send')
        export.set_tooltip_text(_('Export to KML by routes'))
        export.connect('clicked', self.controller.on_export_kml_routes)
        toolbar.add(export)

        toolbar.add(Gtk.SeparatorToolItem())

        return toolbar
