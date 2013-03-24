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

import sys

from gi.repository import Gtk, Champlain, GtkChamplain, Clutter

from StopMarker import StopMarker
from PopupMarker import PopupMarker

class GTMap(GtkChamplain.Embed):
    def __init__(self):
        GtkChamplain.Embed.__init__(self)

        # give ourselves an initial size
        self.set_size_request(640, 480)

        self.view = self.get_view()

        # our bus station layer
        self.stop_layer = Champlain.MarkerLayer()
        self.view.add_layer(self.stop_layer)
        self.stop_layer.show()
        self.stop_layer.show_all_markers()

        # !mwd - temp zoom to birmingham
        self.view.go_to(33.511878, -86.808826)
        self.view.set_zoom_level(14)

        # add a route layer
        self.route_layer = Champlain.PathLayer()
        self.view.add_layer(self.route_layer)
        # add in a path layer
        self.path_layer = Champlain.PathLayer()
        self.path_layer.set_stroke_color(Clutter.Color.new(0x0d, 0xff, 0x0f, 0xbb))
        self.view.add_layer(self.path_layer)

        # our popup layer
        self.popup_layer = Champlain.MarkerLayer()
        self.view.add_layer(self.popup_layer)

        # our big image layer
        self.image_layer = Champlain.MarkerLayer()
        self.view.add_layer(self.image_layer)
        # our picture
        self.picture_group = Clutter.Group()
        self.view.bin_layout_add(self.picture_group, Clutter.BinAlignment.CENTER, Clutter.BinAlignment.CENTER)
        
        self.view.set_kinetic_mode(True)
        self.view.set_reactive(True)


    def add_stop(self, stop):
        m = StopMarker(self, stop)
        self.stop_layer.add_marker(m)
        m.animate_in()

        return m

    def update_stop(self, stop):
        for i in self.stop_layer.get_markers():
            if i.stop == stop:
                i.set_location(stop.latitude, stop.longitude)
                i.update()
                return True
        return False

    def update_stops(self):
        for i in self.stop_layer.get_markers():
            i.update()

    def remove_stop(self, stop):
        m = None
        for i in self.stop_layer.get_markers():
            if i.stop == stop:
                m = i
                break
        if m:
            self.stop_layer.remove_marker(m)

    def show_stop(self, stop):
        for i in self.stop_layer.get_markers():
            if i.stop == stop:
                # zoom here
                #self.view.go_to(i.stop.latitude, i.stop.longitude)
                i.clicked(True)
                break

    def unshow_stop_info(self):
        for m in self.stop_layer.get_markers():
            m.hide()

    def draw_route(self, r):
        if r is None:
            return

        # clear our route layer of any old stuff
        self.route_layer.remove_all()

        for stop in r.stops:
            self.route_layer.add_node(Champlain.Coordinate.new_full(stop.latitude, stop.longitude))
        self.route_layer.show()
        
        # clear our path layer of any old stuff
        self.path_layer.remove_all()
        if r.path is not None and r.path.coords is not None:
            for coord in r.path.coords:
                self.path_layer.add_node(Champlain.Coordinate.new_full(coord[0], coord[1]))
        self.path_layer.show()

        return self.route_layer

    def remove_route(self, route):
        self.route_layer.remove_all()
        self.route_layer.show()
        self.path_layer.remove_all()
        self.path_layer.show()

    def show_popup(self, stop_marker, group):
        if stop_marker is None or group is None:
            return

        self.popup_layer.remove_all()
        group.show_all()
        self.popup_layer.add_marker(PopupMarker(group, stop_marker.stop.latitude, stop_marker.stop.longitude))

        self.popup_layer.show()

    def unshow_popup(self, stop_marker):
        if stop_marker is None:
            return

        self.popup_layer.remove_all()
        self.popup_layer.hide()            
        
    def show_image(self, img):
        self.picture_group.remove_all()

        self.picture_group.add_child(img)
        self.image_layer.show()

    def remove_image(self, img):
        if img:
            self.picture_group.remove_child(img)

        self.image_layer.hide()
