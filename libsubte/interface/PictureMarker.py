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

import EXIF

import libsubte
from Locale import _

import GTGui
from AddStop import AddStop, AddStopDialog

class PictureMarker(Champlain.CustomMarker):
    def __init__(self, gtmap, picture):
        Champlain.CustomMarker.__init__(self)

        self._gtmap = None
        self.gtmap = gtmap

        self.picture = picture

        self.picture_box = None
        self.full_picture_box = None

        self.latitude = 0.0
        self.longitude = 0.0

        # draw our clickable marker
        marker = Clutter.Actor()
        purple = Clutter.Color.new(0xf0, 0x02, 0xf0, 0xbb)
        marker.set_background_color(purple)
        marker.set_size(15, 15)
        marker.set_position(0, 0)
        marker.set_anchor_point(0, 0)
        marker.set_reactive(True)
        self.add_actor(marker)
        marker.show()

        # our meta info
        self.group = Clutter.Group()
        self.group.set_position(20, 0)
        self.group.set_anchor_point(0, 0)
        self.add_actor(self.group)

        # just drawn a rectange or something
        rect = Clutter.Actor()
        c = Clutter.Color()
        c.from_string('#FFFFFFEE')
        rect.set_background_color(c)
        rect.set_size(200, 270)
        rect.set_position(0, 10)
        rect.set_anchor_point(0, 0)
        self.group.add_child(rect)

        self.name = Clutter.Text()
        self.name.set_text('')
        self.name.set_size(190, 25)
        self.name.set_position(20, 15)
        self.name.set_anchor_point(0, 0)
        self.group.add_child(self.name)

        self.info = Clutter.Text()
        self.info.set_use_markup(True)
        self.info.set_text('')
        self.info.set_size(190, 150)
        self.info.set_position(5, 210)
        self.info.set_anchor_point(0, 0)
        self.group.add_child(self.info)

        self.link_stop = Clutter.Text()
        self.link_stop.set_use_markup(True)
        self.link_stop.set_markup('<span foreground="blue">+</span>')
        self.link_stop.set_size(20, 25)
        self.link_stop.set_position(5, 15)
        self.link_stop.set_anchor_point(0, 0)
        #!lukstafi -- changed button-release to button-press
        self.link_stop.connect('button-press-event', self.on_link_stop)
        self.group.add_child(self.link_stop)

        self.unlink_stop = Clutter.Text()
        self.unlink_stop.set_use_markup(True)
        self.unlink_stop.set_markup('<span foreground="blue">X</span>')
        self.unlink_stop.set_size(20, 25)
        self.unlink_stop.set_position(5, 15)
        self.unlink_stop.set_anchor_point(0, 0)
        #!lukstafi -- changed button-release to button-press
        self.unlink_stop.connect('button-press-event', self.on_unlink_stop)
        self.group.add_child(self.unlink_stop)


        self.orientation = 0
        try:
            # get the exif info
            f = open(self.picture.image, 'rb')
            tags = EXIF.process_file(f, details=False)
            if len(tags) == 0:
                raise IOError


            lat = tags.get('GPS GPSLatitude', None)
            lon = tags.get('GPS GPSLongitude', None)
            lat_ref = tags.get('GPS GPSLatitudeRef', 'N')
            lon_ref = tags.get('GPS GPSLongitudeRef', 'W')

            # convert to lat/long
            # from:
            # http://www.nihilogic.dk/labs/gps_exif_google_maps/
            
            i = -1 if lat_ref is 'N' else 1
            flat = ((lat.values[0].num / float(lat.values[0].den)) + \
                        ((lat.values[1].num / float(lat.values[1].den)) / 60.0) + \
                        ((lat.values[2].num /float(lat.values[2].den)) / 3600.0)) * i

            j = 1 if lon_ref is 'W' else -1
            flon = ((lon.values[0].num / float(lon.values[0].den)) + \
                        ((lon.values[1].num / float(lon.values[1].den)) / 60.0) + \
                        ((lon.values[2].num /float(lon.values[2].den)) / 3600.0)) * j

            self.latitude = flat
            self.longitude = flon

            self.info.set_markup('<markup><big><b>GPS Info:</b></big>\n<b>Latitude:</b> %s\n<b>Longitude:</b> %s</markup>' % (self.latitude, self.longitude))

            # orientation
            orientation_tag = tags.get('Image Orientation', None)
            
            if orientation_tag is not None:
                orientation_v = orientation_tag.values

                if orientation_v[0] == 8: # counter clock wise
                    self.orientation = -90
                    #self.picture.set_z_rotation_from_gravity(-90, Clutter.Gravity.CENTER)
                elif orientation_v[0] == 6: # clock wise
                    #self.picture.set_z_rotation_from_gravity(90, Clutter.Gravity.CENTER)
                    self.orientation = 90
                elif orientation_v[0] == 3: # 180
                    #self.picture.set_z_rotation_from_gravity(180, Clutter.Gravity.CENTER)
                    self.orientation = 180

        except IOError, e:
            print >> sys.stderr, 'No GPS tags?', e

        # hide our meta
        self.group.hide_all()
        self._visible = False

        # our position
        self.set_location(self.latitude, self.longitude)
        
        #!lukstafi -- changed button-release to button-press
        marker.connect('button-press-event', self.on_click)

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

    def on_link_stop(self, actor, event):
        print >> sys.stderr, 'Link stop'

        gtgui = GTGui.GTGui.instance()

        stop_dialog = AddStop(gtgui.controller)

        win = AddStopDialog(gtgui)
        # set the lat/long
        stop_dialog.latitude_txt.set_text('%s' % self.latitude)
        stop_dialog.longitude_txt.set_text('%s' % self.longitude)
        win.get_content_area().pack_start(stop_dialog, True, True, 5)

        # We can't seem to pop up a dialog in a callback
        #  here, it freezes everything. Instead, run the
        #  dialog, and set an on_reponse so that
        #  we get the response code when it closes
        def on_response(win, resp, user_data = None):
            print >> sys.stderr, 'on response', resp
            if resp == Gtk.ResponseType.ACCEPT:
                print >> sys.stderr, 'resp is ACCEPT', resp
                # create a new stop
                s = libsubte.Stop(name = stop_dialog.get_name(),
                                   description = stop_dialog.get_description(),
                                   latitude = stop_dialog.get_latitude(),
                                   longitude = stop_dialog.get_longitude())

                self.picture.stop = s

                gtgui.controller.add_stop(s)

            win.destroy()
            

        win.connect('response', on_response)
        win.show_all()


        return False
    def on_unlink_stop(self, actor, event):
        print >> sys.stderr, 'Unlink stop'
        if self.picture.stop:
            self.picture.stop = None

        # update our text
        self.on_click(None, None)
        self.on_click(None, None)

        return False

    def on_click(self, actor, event):
        self._visible = not self._visible

        # disable somethings
        self.link_stop.set_reactive(False)
        self.unlink_stop.set_reactive(False)

        if self._visible:
            self.gtmap.unshow_pictures()

            # we are visible
            self._visible = True

            # update our name
            if self.picture.stop:
                self.name.set_text('%s) Stop: (%s) %s' % (self.picture.picture_id, self.picture.stop.stop_id, self.picture.stop.name))
            else:
                self.name.set_text('(%s) No Stop Linked' % self.picture.picture_id)

            # create our texture
            try:
                self.picture_box = Clutter.Texture()
                if self.picture.thumbnail:
                    self.picture_box.set_from_file(self.picture.thumbnail)
                else:
                    self.picture_box.set_from_file(self.picture.image)
                self.picture_box.set_keep_aspect_ratio(True)
                #self.picture_box.set_size(150, 150)
                self.picture_box.set_width(150)
                self.picture_box.set_position(25, 60)
                self.picture_box.set_anchor_point(0, 0)
                self.picture_box.set_z_rotation_from_gravity(self.orientation, Clutter.Gravity.CENTER)
                #!lukstafi -- changed button-release to button-press
                self.picture_box.connect('button-press-event', self.on_expand_picture)
                self.picture_box.set_reactive(True)
                self.group.add_child(self.picture_box)
            except GLib.GError, e:
                print >> sys.stderr, e
                #!mwd - load a broken image instead?

            self.group.show_all()

            if self.picture.stop:
                self.link_stop.hide()
                self.unlink_stop.set_reactive(True)
            else:
                self.unlink_stop.hide()
                self.link_stop.set_reactive(True)
        else:
            self.hide()

        return True

    def on_expand_picture(self, actor, event):
        self.full_picture_box = Clutter.Texture()
        self.full_picture_box.set_from_file(self.picture.image)
        self.full_picture_box.set_keep_aspect_ratio(True)

        size = self.gtmap.get_allocated_width(), self.gtmap.get_allocated_height()
        r1 = size[0] / float(size[1])
        size2 = self.full_picture_box.get_base_size()

        if self.orientation == 0 or self.orientation == 180:
            r2 = size2[0] / float(size2[1])
        else:
            r2 = size2[1] / float(size2[0])

        self.full_picture_box.set_position(0, 0)
        self.full_picture_box.set_z_rotation_from_gravity(self.orientation, Clutter.Gravity.CENTER)

        if r1 > r2: # use width
            w = size[1] * r2
            h = size[1] 
        else: # use height
            w = size[0]
            h = size[0] / r2

        if self.orientation != 0 and self.orientation != 180:
            w, h = h, w # reverse
        self.full_picture_box.set_size(w, h)


        self.full_picture_box.set_reactive(True)
        #!lukstafi -- changed button-release to button-press
        self.full_picture_box.connect('button-press-event', self.on_close_picture)
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
        pass

    def hide(self):
        self.group.hide_all()
        if self.picture_box:
            self.group.remove_child(self.picture_box)
            self.picture_box = None

        self._visible = False
