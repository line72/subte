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

from gi.repository import Gtk, Champlain, GtkChamplain, Clutter

from PictureMarker import PictureMarker

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

        # our picture of stops layer
        self.picture_layer = Champlain.MarkerLayer()
        self.view.add_layer(self.picture_layer)
        self.picture_layer.show()
        self.picture_layer.show_all_markers()
        # temp add one
        marker = PictureMarker()
        marker.set_location(33.511, -86.808)
        self.picture_layer.add_marker(marker)
        marker.animate_in()

        # !mwd - temp zoom to birmingham
        self.view.go_to(33.511878, -86.808826)
        self.view.set_zoom_level(14)

        # add a route layer
        self.route_layer = Champlain.PathLayer()
        self.view.add_layer(self.route_layer)
        
        self.view.set_kinetic_mode(True)
        self.view.set_reactive(True)


    def on_click(self, view, event):
        print 'on-click', view, event

        print view.x_to_longitude(event.x), view.y_to_latitude(event.y)

        # add a random place maker
        import random

        purple = Clutter.Color.new(0xf0, 0x02, 0xf0, 0xbb)

        marker = Champlain.Label.new_with_text('Stop %d' % random.randint(0, 1000),
                                               'Serif 14', None, purple)
        marker.set_use_markup(True)
        marker.set_color(purple)
        marker.set_location(view.y_to_latitude(event.y), view.x_to_longitude(event.x))
        marker.set_reactive(True)
        marker.connect('button-release-event', self.on_marker_click)
        self.stop_layer.add_marker(marker)

        #self.stop_layer.animate_in_all_markers()
        marker.animate_in()
        print 'marker=', marker

        return True

    def add_stop(self, stop):
        purple = Clutter.Color.new(0xf0, 0x02, 0xf0, 0xbb)
        yellow = Clutter.Color.new(0xce, 0xe7, 0x51, 0xbb)

        name = stop.name
        if name is None:
            name = stop.id
        #marker = Champlain.Label.new_with_text('(%d) %s' % (stop.id, name),
        #                                       'Serif 10', None, purple)
        marker = Champlain.Point.new()
        #marker.set_use_markup(True)
        marker.set_color(purple)
        marker.set_selection_color(yellow)
        marker.set_location(stop.latitude, stop.longitude)
        marker.set_reactive(True)
        #marker.connect('button-release-event', self.on_marker_click)
        self.stop_layer.add_marker(marker)

        marker.animate_in()

        return marker

    def remove_stop(self, stop):
        pass

    def draw_route(self, r):
        if r is None:
            return

        # clear our route layer of any old stuff
        self.route_layer.remove_all()

        for stop in r.stops:
            self.route_layer.add_node(Champlain.Coordinate.new_full(stop.latitude, stop.longitude))
        self.route_layer.show()
        
        return self.route_layer

    def remove_route(self, route):
        self.route_layer.remove_all()
        self.route_layer.show()

    def on_marker_click(self, actor, event):
        print 'on_marker_click', actor, event

        return False
    
