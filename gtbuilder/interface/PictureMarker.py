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

from gi.repository import Gtk, Champlain, Clutter

class PictureMarker(Champlain.CustomMarker):
    def __init__(self):
        Champlain.CustomMarker.__init__(self)

        # draw our clickable marker
        marker = Clutter.Actor()
        purple = Clutter.Color.new(0xf0, 0x02, 0xf0, 0xbb)
        marker.set_background_color(purple)
        marker.set_size(15, 15)
        marker.set_position(0, 0)
        marker.set_anchor_point(0, 0)
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
        c.from_string('#33FF33AA')
        rect.set_background_color(c)
        rect.set_size(100, 100)
        rect.set_position(0, 0)
        rect.set_anchor_point(0, 0)
        self.group.add_child(rect)

        # hide our meta
        self.group.hide_all()
        self._visible = False

        self.connect('button-release-event', self.on_click)

    def on_click(self, actor, event):
        print 'on click', self._visible, actor, event
        self._visible = not self._visible

        if self._visible:
            self.group.show_all()
        else:
            self.group.hide_all()

        return True

