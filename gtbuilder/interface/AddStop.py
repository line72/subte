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

import gtbuilder

class AddStopDialog(Gtk.Dialog):
    def __init__(self, *args, **kwds):
        Gtk.Dialog.__init__(self, args, kwds)

        self.add_button('Add', Gtk.ResponseType.ACCEPT)
        self.add_button('Cancel', Gtk.ResponseType.CANCEL)

class AddStop(Gtk.VBox):
    '''A dialog that creates a new stop'''
    def __init__(self, controller):
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
