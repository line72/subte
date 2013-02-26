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
import math
import weakref

from gi.repository import Gtk, Champlain, Clutter, GLib

import libsubte
import shapes

class StopMarker(Champlain.CustomMarker):
    def __init__(self, gtmap, stop):
        Champlain.CustomMarker.__init__(self)

        self._gtmap = None
        self.gtmap = gtmap

        self._stop = None
        self.stop = stop

        self.full_picture_box = None

        self.unselected_color = Clutter.Color.new(0xf0, 0x02, 0xf0, 0xbb)
        self.selected_color = Clutter.Color.new(0xfd, 0xfd, 0x02, 0xbb)
        

        # draw our clickable marker
        self.marker = Clutter.Actor()
        self.marker.set_background_color(self.unselected_color)
        self.marker.set_size(16, 16)
        self.marker.set_position(0, 0)
        self.marker.set_anchor_point(8, 8)
        self.marker.set_reactive(True)
        self.add_actor(self.marker)
        self.marker.show()

        self._visible = False

        self.set_location(self.stop.latitude, self.stop.longitude)

        # trying to capture it, then make us emit a signal doesn't
        #  seem to be working
        #self.marker.connect('button-release-event', self.on_click)

        self.set_reactive(False)

    @property
    def gtmap(self):
        if self._gtmap:
            return self._gtmap()
        return None
    @gtmap.setter
    def gtmap(self, m):
        if m:
            self._gtmap = weakref.ref(m)
        else:
            self._gtmap = None

    @property
    def stop(self):
        if self._stop:
            return self._stop()
        return None
    @stop.setter
    def stop(self, m):
        if m:
            self._stop = weakref.ref(m)
        else:
            self._stop = None
            
    def selected(self, status):
        if status:
            self.marker.set_background_color(self.selected_color)
        else:
            self.marker.set_background_color(self.unselected_color)
        return True

    def clicked(self, status):
        if status == self._visible: # nothing to do here
            return True

        if status:
            self.show()
        else:
            self.hide()

        return True

    def on_click(self, actor, event, user_data = None):
        #!mwd - this doesn't work :(
        print 'on_click and emitting', actor, event
        self.emit('button-release-event', event)
        return True

    def on_expand_picture(self, actor, event, picture):
        self.full_picture_box = Clutter.Texture()
        self.full_picture_box.set_from_file(picture.image)
        self.full_picture_box.set_keep_aspect_ratio(True)

        size = self.gtmap.get_allocated_width(), self.gtmap.get_allocated_height()
        r1 = size[0] / float(size[1])
        size2 = self.full_picture_box.get_base_size()

        if picture.orientation == 0 or picture.orientation == 180:
            r2 = size2[0] / float(size2[1])
        else:
            r2 = size2[1] / float(size2[0])

        self.full_picture_box.set_position(0, 0)
        self.full_picture_box.set_z_rotation_from_gravity(picture.orientation, Clutter.Gravity.CENTER)

        if r1 > r2: # use width
            w = size[1] * r2
            h = size[1] 
        else: # use height
            w = size[0]
            h = size[0] / r2

        if picture.orientation != 0 and picture.orientation != 180:
            w, h = h, w # reverse
        self.full_picture_box.set_size(w, h)


        self.full_picture_box.set_reactive(True)
        self.full_picture_box.connect('button-release-event', self.on_close_picture)
        self.full_picture_box.show_all()

        self.gtmap.show_image(self.full_picture_box)

        return False

    def on_close_picture(self, actor, event):
        if self.full_picture_box:
            self.gtmap.remove_image(self.full_picture_box)
            self.full_picture_box.hide_all()
        self.full_picture_box = None

        return False

    def show(self):
        self.gtmap.unshow_stop_info()

        width = 500
        height = 200

        # our meta info
        group = Clutter.Group()
        group.set_position(8, -8)
        group.set_anchor_point(width / 2, height)

        # just drawn a rectange or something
        rect = shapes.Bubble()
        c = Clutter.Color.new(0xde, 0xde, 0xde, 0xfe)
        rect.set_color(c)
        rect.set_has_outline(True)
        rect.set_outline_color(Clutter.Color.new(0x00, 0x00, 0x00, 0xff))
        rect.set_size(width, height)
        rect.set_position(0, 8)
        rect.set_anchor_point(0, 0)
        rect.set_has_shadow(True)
        group.add_child(rect)

        name = Clutter.Text()
        if self.stop.name:
            name.set_markup('<markup><b>%s</b></markup>' % self.stop.name.replace('&', '&amp;'))
        else:
            name.set_markup('<markup><b>%s</b></markup>' % self.stop.stop_id)
        name.set_size(400, 25)
        name.set_position(10, 15)
        name.set_anchor_point(0, 0)
        group.add_child(name)

        info = Clutter.Text()
        info.set_use_markup(True)
        info.set_text('')
        info.set_size(200, 75)
        info.set_position(10, 50)
        info.set_anchor_point(0, 0)
        group.add_child(info)

        info.set_markup('<markup><b>Latitude:</b> %s\n<b>Longitude:</b> %s</markup>' % (self.stop.latitude, self.stop.longitude))

        routes = Clutter.Text()
        if len(self.stop.routes) > 0:
            route_names = ', '.join([x.short_name for x in self.stop.routes])
        else:
            route_names = 'None'
        routes.set_markup('<markup><b>Routes:</b> %s</markup>' % route_names)
        routes.set_size(200, 75)
        routes.set_position(10, 100)
        routes.set_anchor_point(0, 0)
        group.add_child(routes)

        # see if we have a picture (or more)
        if len(self.stop.pictures) > 0:
            try:
                picture_box = Clutter.Texture()

                # just use the first picture for now
                picture = self.stop.pictures[0]

                if picture.thumbnail:
                    picture_box.set_from_file(picture.thumbnail)
                else:
                    picture_box.set_from_file(picture.image)

                w, h = picture_box.get_base_size()
                picture_box.set_keep_aspect_ratio(True)
                picture_box.set_anchor_point(0, 0)
                if picture.orientation in (90, -90):
                    #!mwd - I have no idea how the fuck clutter is rotation this
                    #  It seems as though the bounding box doesn't change
                    #  so I'm just making up some position numbers
                    picture_box.set_width(100)
                    picture_box.set_position(width - ((h/w) * 100) - (w/2) - 45, 60)
                    picture_box.set_z_rotation_from_gravity(picture.orientation, Clutter.Gravity.CENTER)
                else:
                    picture_box.set_height(100)
                    picture_box.set_position(width - ((w/h) * 100) - (w/2) - 25, 50)

                picture_box.connect('button-release-event', self.on_expand_picture, picture)
                picture_box.set_reactive(True)
                group.add_child(picture_box)
            except GLib.GError, e:
                print >> sys.stderr, 'Error loading image', e

        self.gtmap.show_popup(self, group)

        self._visible = True

    def hide(self):
        self.gtmap.unshow_popup(self)
            
        self._visible = False
