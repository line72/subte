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

import random
import weakref
import os
import md5
import sys

from gi.repository import Gtk

import libsubte

from AddStop import AddStopDialog, EditStopDialog, AddStop
from AddRoute import AddRouteDialog, EditRouteDialog, AddRoute
from MergeStops import MergeStopsDialog, MergeStops
from TripList import TripListDialog, TripList
from TripRouteDialog import AddTripRouteDialog, EditTripRouteDialog

from KMLParser import KMLParser

class Controller(object):
    '''This is a controller class. It handles all the callbacks
    from the GUI'''
    class SignalHandler(object):
        def __init__(self, fn, args):
            self._fn = fn
            self._args = args

    def __init__(self, gui):
        self._gui = weakref.ref(gui)
        self._registered_events = {}

        self._selected_stops = []

    def initialize(self):
        # fill in the initial data
        # stops first
        for s in libsubte.Stop.stops:
            self.add_stop(s)
        # trips
        for t in libsubte.TripRoute.trip_routes:
            self.add_trip(t)
        # and paths
        for p in libsubte.Path.paths:
            self.add_path(p)

        # update all the stops
        self.gui.map_widget.update_stops()

    def connect(self, signal, fn, *args):
        if signal not in self._registered_events:
            self._registered_events[signal] = []

        handler = Controller.SignalHandler(fn, args)
        self._registered_events[signal].append(handler)

        return handler

    def disconnect(self, signal, handler):
        try:
            self._registered_events[signal].remove(handler)
        except Exception:
            pass

    def on_map_click(self, view, event, gtmap):
        for handler in self._registered_events.get('on-map-clicked', []):
            handler._fn(view, event, *(handler._args))

        gtmap.unshow_stop_info()

        return True

    def on_stop_marker_clicked(self, actor, event, marker, stop):
        print 'on_stop_marker_clicked', self, actor, event, stop

        # select the list widget
        #  This will calls its callback
        #  which properly centers the map and
        #  shows everything
        self.gui.stop_list_widget.set_selected(stop)

        return True

    def on_stop_list_selected(self, treeview, user_data = None):
        s = self.gui.stop_list_widget.get_selected()

        # hi-light it?
        if s:
            self.gui.map_widget.show_stop(s)

            for handler in self._registered_events.get('on-stop-selected', []):
                handler._fn(s, *(handler._args))

        return True

    def on_route_trip_list_selected(self, treeview, user_data = None):
        r = self.gui.trip_list_widget.get_selected()

        self.gui.map_widget.draw_trip(r)

        return True

    def on_load_project_clicked(self, toolbutton, user_data = None):
        # !mwd - pop up a file dialog
        dlg = Gtk.FileChooserDialog("Open a Subte project",
                                    self.gui, Gtk.FileChooserAction.OPEN,
                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                     Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))
        dlg.show_all()

        if dlg.run() == Gtk.ResponseType.ACCEPT:
            fname = dlg.get_filename()

            # clear
            if self.clear_project(True) == False: # they cancelled saving, don't clear it
                dlg.destroy()
                return True

            # !mwd - pop up a loading dialog
            

            # load
            self.gui.db.load(fname)
            self.initialize()

            # close the loading dialog
        

        dlg.destroy()

        return True

    def on_save_project_clicked(self, toolbutton, user_data = None):
        return self.save_project()

    def on_close_project_clicked(self, toolbutton, user_data = None):
        self.clear_project(True)

        return True

    def on_add_stop_clicked(self, toolbutton, user_data = None):
        print 'adding a stop'
        stop_dialog = AddStop(self)

        win = AddStopDialog(self._gui())
        win.get_content_area().pack_start(stop_dialog, True, True, 5)
        win.show_all()

        handler = self.connect('on-map-clicked', stop_dialog.on_map_clicked)

        resp = win.run()
        self.disconnect('on-map-clicked', handler)

        if resp == Gtk.ResponseType.ACCEPT:
            # create a new stop
            s = libsubte.Stop(name = stop_dialog.get_name(),
                               description = stop_dialog.get_description(),
                               latitude = stop_dialog.get_latitude(),
                               longitude = stop_dialog.get_longitude())
            
            self.add_stop(s)

        win.destroy()

    def on_edit_stop_clicked(self, toolbutton, user_data = None):
        print 'on edit stop'

        stop = self.gui.stop_list_widget.get_selected()
        if stop is None:
            return True

        stop_dialog = AddStop(self, stop)

        win = EditStopDialog(self._gui())
        win.get_content_area().pack_start(stop_dialog, True, True, 5)
        win.show_all()

        handler = self.connect('on-map-clicked', stop_dialog.on_map_clicked)

        resp = win.run()
        self.disconnect('on-map-clicked', handler)

        if resp == Gtk.ResponseType.ACCEPT:
            # update the stop
            stop.name = stop_dialog.get_name()
            stop.description = stop_dialog.get_description()
            stop.latitude = stop_dialog.get_latitude()
            stop.longitude = stop_dialog.get_longitude()

            # update the stop
            self.update_stop(stop)

        win.destroy()

    def on_remove_stop_clicked(self, toolbutton, user_data = None):
        print 'removing stop'
        stop = self.gui.stop_list_widget.get_selected()
        if stop is None:
            print 'Nothing selected'
            return

        # good-bye
        try:
            print 'destroying'
            if stop.is_orphan():

                # destroy
                stop.destroy()

                # remove from interface
                self.gui.map_widget.remove_stop(stop)
                self.gui.stop_list_widget.remove_stop(stop)


        except Exception, e:
            print 'Stop is in use by route'

    def on_merge_stops_clicked(self, toolbutton, user_data = None):
        print 'merging stops'

        # open the dialog
        merge_stop_dialog = MergeStops(self)

        win = MergeStopsDialog(self._gui())
        win.get_content_area().pack_start(merge_stop_dialog, True, True, 5)

        handler = self.connect('on-stop-selected', merge_stop_dialog.on_stop_selected)

        def on_response(widget, response_id, dlg, handler):
            if response_id == Gtk.ResponseType.ACCEPT:
                print 'merging', dlg.stop1, dlg.stop2
                if dlg.stop1 and dlg.stop2:
                    dlg.stop1.merge_with(dlg.stop2)

                    # destroy
                    dlg.stop2.destroy()
                    # remove from interface
                    self.gui.map_widget.remove_stop(dlg.stop2)
                    self.gui.stop_list_widget.remove_stop(dlg.stop2)

                else:
                    print 'Invalid stops selected'

            widget.destroy()
            self.disconnect('on-stop-selected', handler)

        win.connect('response', on_response, merge_stop_dialog, handler)

        win.show_all()

    def on_add_trip_clicked(self, toolbutton, user_data = None):
        # create the trip (temporarily)
        try: route = Route.routes[0]
        except Exception, e: route = None

        try: calendar = Calendar.calendars[0]
        except Exception, e: calendar = None

        trip = libsubte.TripRoute('', route, calendar, '', 0, None)

        win = AddTripRouteDialog(self._gui(), trip)
        win.show_all()

        dlg = win.content

        handler = self.connect('on-stop-selected', dlg.on_stop_selected)

        resp = win.run()
        self.disconnect('on-stop-selected', handler)

        if resp == Gtk.ResponseType.ACCEPT:
            name = dlg.get_name()
            route = dlg.get_route()
            calendar = dlg.get_calendar()
            headsign = dlg.get_headsign()
            direction = dlg.get_direction()
            path = dlg.get_path()

            if route != trip.route and route != None:
                if trip.route:
                    trip.route.remove_trip_route(trip)
                route.add_trip_route(trip)

            trip.name = name
            trip.route = route
            trip.calendar = calendar
            trip.headsign = headsign
            trip.direction = direction
            trip.path = path

            self.add_trip(trip)
        else:
            trip.destroy()

        win.destroy()

        return True

    def on_edit_trip_clicked(self, toolbutton, user_data = None):
        trip = self.gui.trip_list_widget.get_selected()
        if trip is None:
            return True

        win = EditTripRouteDialog(self._gui(), trip)
        win.show_all()

        dlg = win.content

        handler = self.connect('on-stop-selected', dlg.on_stop_selected)

        resp = win.run()
        self.disconnect('on-stop-selected', handler)

        if resp == Gtk.ResponseType.ACCEPT:
            name = dlg.get_name()
            route = dlg.get_route()
            calendar = dlg.get_calendar()
            headsign = dlg.get_headsign()
            direction = dlg.get_direction()
            path = dlg.get_path()

            if route != trip.route:
                trip.route.remove_trip_route(trip)
                route.add_trip_route(trip)

            trip.name = name
            trip.route = route
            trip.calendar = calendar
            trip.headsign = headsign
            trip.direction = direction
            trip.path = path

            self.update_trip(trip)

        win.destroy()

        return True

    def on_remove_trip_clicked(self, toolbutton, user_data = None):
        trip_route = self.gui.trip_list_widget.get_selected()
        if trip_route is None:
            return True

        if trip_route.route:
            trip_route.route.remove_trip_route(trip_route)

        self.remove_trip(trip_route)

        return True

    def on_copy_trip_clicked(self, toolbutton, user_data = None):
        trip_route = self.gui.trip_list_widget.get_selected()
        if trip_route is None:
            return True

        trip_route_copy = trip_route.copy()
        self.add_trip(trip_route_copy)

        return True

    def on_add_picture_clicked(self, toolbutton, user_data = None):
        print 'on add picture'
        # pop up a load dialg
        dlg = Gtk.FileChooserDialog('Import from...', self._gui(),
                                    Gtk.FileChooserAction.SELECT_FOLDER,
                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                     Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))

        resp = dlg.run()
        if resp == Gtk.ResponseType.ACCEPT:
            directory = dlg.get_filename()
            
            # iterate through all the .jpg files
            for i in os.listdir(directory):
                if not i.lower().endswith('.jpg'):
                    continue

                im = os.path.join(directory, i)

                # check for a duplicate
                f = open(im, 'rb')
                md5sum = md5.md5(f.read()).hexdigest()
                if libsubte.Picture.is_duplicate(md5sum):
                    continue
                
                # load it!
                p = libsubte.Picture(im)
                # now create a new stop associated with this picture
                s = libsubte.Stop(latitude = p.latitude, longitude = p.longitude)
                s.add_picture(p)

                # add it
                self.add_stop(s)
            
        dlg.destroy()

    # def on_remove_picture_clicked(self, toolbutton, user_data = None):
    #     print 'on remove picture'
    #     picture = self.gui.picture_list_widget.get_selected()
    #     if picture is None:
    #         print 'Nothing selected'
    #         return

    #     # remove this from our widgets
    #     self.gui.map_widget.remove_picture(picture)
    #     self.gui.picture_list_widget.remove_picture(picture)

    #     # good-bye
    #     picture.destroy()

    def on_add_path_clicked(self, toolbutton, user_data = None):
        dlg = Gtk.FileChooserDialog('Import from...', self._gui(),
                                    Gtk.FileChooserAction.OPEN,
                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                     Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))
        resp = dlg.run()

        if resp == Gtk.ResponseType.ACCEPT:
            try:
                kml_parser = KMLParser()
                paths = kml_parser.parse(dlg.get_filename())

                for p in paths:
                    self.add_path(p)

            except Exception, e:
                print >> sys.stderr, 'Error parsing kml data', e

        dlg.destroy()

        return True

    def on_remove_path_clicked(self, toolbuton, user_data = None):
        path = self.gui.path_list_widget.get_selected()
        if path is None:
            return True

        self.gui.path_list_widget.remove_path(path)

        # make sure no routes use this
        for r in libsubte.Route.routes:
            if r.path == path:
                r.path = None

        path.destroy()

        return True

    def on_export(self, toolbutton, user_data = None):
        # pop up a save dialg
        dlg = Gtk.FileChooserDialog('Export to...', self._gui(),
                                    Gtk.FileChooserAction.SELECT_FOLDER,
                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                     Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))
        resp = dlg.run()
        if resp == Gtk.ResponseType.ACCEPT:
            directory = dlg.get_filename()
            libsubte.Database.export(directory)

        dlg.destroy()

        return True

    def on_import_gtfs(self, toolbutton, user_data = None):
        # pop up an open dialog
        dlg = Gtk.FileChooserDialog('Import from...', self._gui(),
                                    Gtk.FileChooserAction.SELECT_FOLDER,
                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                     Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))
        resp = dlg.run()
        if resp == Gtk.ResponseType.ACCEPT:
            directory = dlg.get_filename()
            libsubte.Database.import_gtfs(directory)

            # remove everything from the gui
            self.gui.map_widget.clear_all()
            self.gui.stop_list_widget.clear_model()
            self.gui.trip_list_widget.clear_model()
            self.gui.path_list_widget.clear_model()
            # re-initialize it
            self.initialize()

        dlg.destroy()

        return True

    def add_stop(self, s):
        m = self.gui.map_widget.add_stop(s)
        #!mwd - this doesn't work since we have a custom marker
        #m.connect('button-release-event', self.on_stop_marker_clicked, s)
        m.marker.connect('button-release-event', self.on_stop_marker_clicked, m, s)
        self.gui.stop_list_widget.add_stop(s)

    def update_stop(self, s):
        self.gui.map_widget.update_stop(s)
        self.gui.stop_list_widget.update_stop(s)

    def add_trip(self, t):
        path = self.gui.map_widget.draw_trip(t)
        self.gui.trip_list_widget.add_trip_route(t)

    def update_trip(self, t):
        path = self.gui.map_widget.draw_trip(t)
        self.gui.trip_list_widget.update_trip_route(t)

    def remove_trip(self, t):
        self.gui.map_widget.remove_trip(t)
        self.gui.trip_list_widget.remove_trip_route(t)

        t.destroy()

    def add_path(self, p):
        self.gui.path_list_widget.add_path(p)

    def save_project(self):
        if self.gui.db.is_open:
            self.gui.db.save()
        else:
            dlg = Gtk.FileChooserDialog("Save a Subte project",
                                    self.gui, Gtk.FileChooserAction.SAVE,
                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                     Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))
            dlg.set_do_overwrite_confirmation(True)

            if self.gui.db.dbname:
                dlg.set_filename(self.gui.db.dbname)

            dlg.show_all()

            if dlg.run() == Gtk.ResponseType.ACCEPT:
                fname = dlg.get_filename()

                self.gui.db.save_as(fname)

            dlg.destroy()

        return True


    def clear_project(self, ask_if_open = True):
        if ask_if_open and self.gui.db.is_empty() == False:
            save_msg = "Save As"
            if self.gui.db.is_open:
                save_msg = "Save"

            dlg = Gtk.MessageDialog(self.gui, Gtk.DialogFlags.MODAL,
                                    Gtk.MessageType.QUESTION,
                                    Gtk.ButtonsType.NONE,
                                    "Would you like to save this project?")
            dlg.add_buttons("Close without Saving", Gtk.ResponseType.REJECT,
                            "Cancel", Gtk.ResponseType.CANCEL,
                            save_msg, Gtk.ResponseType.ACCEPT)
            dlg.set_default_response(Gtk.ResponseType.CANCEL)

            resp = dlg.run()
            if resp == Gtk.ResponseType.CANCEL: # don't do anything, return
                dlg.destroy()
                return False
            elif resp == Gtk.ResponseType.ACCEPT: # save it
                self.save_project()
            elif resp == Gtk.ResponseType.REJECT: # clear it without saving
                pass

            dlg.destroy()               
        
        self.gui.db.close()

        # remove everything from the gui
        self.gui.map_widget.clear_all()
        self.gui.stop_list_widget.clear_model()
        self.gui.trip_list_widget.clear_model()
        self.gui.path_list_widget.clear_model()

        return True

    gui = property(lambda x: x._gui(), None)
