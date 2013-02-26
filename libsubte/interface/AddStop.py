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

import weakref

from gi.repository import Gtk

import libsubte

class AddStopDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, 'Add Stop', parent,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            ('Add', Gtk.ResponseType.ACCEPT,
                            'Cancel', Gtk.ResponseType.CANCEL))

class EditStopDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, 'Edit Stop', parent,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            ('Edit', Gtk.ResponseType.ACCEPT,
                            'Cancel', Gtk.ResponseType.CANCEL))

class AddStop(Gtk.VBox):
    '''A dialog that creates a new stop'''
    def __init__(self, controller, stop = None):
        Gtk.VBox.__init__(self, False)
        
        self._controller = weakref.ref(controller)

        size_group = Gtk.SizeGroup(mode = Gtk.SizeGroupMode.HORIZONTAL)

        # name
        hbox = Gtk.HBox(False)
        name_lbl = Gtk.Label('Name: ')
        size_group.add_widget(name_lbl)       
        hbox.pack_start(name_lbl, False, False, 0)
        self.name_txt = Gtk.Entry()
        hbox.pack_start(self.name_txt, True, True, 5)

        self.pack_start(hbox, True, True, 5)

        # description
        hbox = Gtk.HBox(False)
        description_lbl = Gtk.Label('Description: ')
        size_group.add_widget(description_lbl)       
        hbox.pack_start(description_lbl, False, False, 0)
        self.description_txt = Gtk.TextView()
        hbox.pack_start(self.description_txt, True, True, 5)

        self.pack_start(hbox, True, True, 5)

        # lat long
        hbox = Gtk.HBox(False)
        lat_lbl = Gtk.Label('Latitude: ')
        size_group.add_widget(lat_lbl)
        hbox.pack_start(lat_lbl, False, False, 0)
        self.latitude_txt = Gtk.Entry()
        hbox.pack_start(self.latitude_txt, True, True, 5)

        long_lbl = Gtk.Label('Longitude: ')
        size_group.add_widget(long_lbl)
        hbox.pack_start(long_lbl, False, False, 0)
        self.longitude_txt = Gtk.Entry()
        hbox.pack_start(self.longitude_txt, True, True, 5)

        self.pack_start(hbox, True, True, 5)

        self._fill(stop)

    def get_name(self):
        return self.name_txt.get_text()

    def get_description(self):
        b = self.description_txt.get_buffer()
        return b.get_text(b.get_start_iter(), b.get_end_iter(), False)

    def set_description(self, desc):
        b = Gtk.TextBuffer()
        b.set_text(desc)
        self.description_txt.set_buffer(b)

    def get_latitude(self):
        return float(self.latitude_txt.get_text())
    def get_longitude(self):
        return float(self.longitude_txt.get_text())

    def on_map_clicked(self, view, event):
        print 'on_map_clicked', view, event

        latitude = view.y_to_latitude(event.y)
        longitude = view.x_to_longitude(event.x)

        print latitude, longitude
        self.latitude_txt.set_text(str(latitude))
        self.longitude_txt.set_text(str(longitude))
        
    def _fill(self, stop):
        if stop is None:
            return

        self.name_txt.set_text(stop.name)
        self.set_description(stop.description)
        self.latitude_txt.set_text('%s' % stop.latitude)
        self.longitude_txt.set_text('%s' % stop.longitude)
