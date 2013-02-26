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

from gi.repository import Gtk

import libsubte

class PathChoice(Gtk.HBox):
    def __init__(self):
        Gtk.HBox.__init__(self, False)

        self.lbl = Gtk.Label('Path: ')
        self.pack_start(self.lbl, False, False, 0)

        # our choices
        self.choice = Gtk.ComboBoxText.new()
        self.pack_start(self.choice, True, True, 5)

        # add our paths
        self.choice.append_text('') # blank for None
        for path in libsubte.Path.paths:
            #!mwd - we shouldn't be referencing by name 
            #  but by id, just incase we have two with the 
            #  same name
            self.choice.append_text(path.name)
        self.choice.set_active(0)

    def get_label(self):
        return self.lbl

    def get_selection(self):
        selection = self.choice.get_active_text()
        for path in libsubte.Path.paths:
            if path.name == selection:
                return path
        return None

    def set_selection(self, v):
        model = self.choice.get_model()
        it = model.get_iter_first()
        while it:
            if model.get_value(it, 0) == v:
                self.choice.set_active_iter(it)
                return True
            it = model.iter_next(it)
        return False

