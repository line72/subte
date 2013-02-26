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

class AddAgencyDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, 'Add Agency', parent,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            ('Add', Gtk.ResponseType.ACCEPT,
                             'Cancel', Gtk.ResponseType.CANCEL))

        self.content = AddAgency()
        self.get_content_area().add(self.content)

class AddAgency(Gtk.VBox):
    '''A vbox for adding an agency'''
    def __init__(self):
        Gtk.VBox.__init__(self, False)

        size_group = Gtk.SizeGroup(mode = Gtk.SizeGroupMode.HORIZONTAL)

        # name
        hbox = Gtk.HBox(False)
        name_lbl = Gtk.Label('Name: ')
        size_group.add_widget(name_lbl)       
        hbox.pack_start(name_lbl, False, False, 0)
        self.name_txt = Gtk.Entry()
        hbox.pack_start(self.name_txt, True, True, 5)
        self.pack_start(hbox, True, True, 5)

        # url

        # timezone

        # language

        # phone

        # fare url

    name = property(lambda x: x.name_txt.get_text(), None)


class AgencyChoice(Gtk.HBox):
    def __init__(self):
        Gtk.HBox.__init__(self, False)

        self.lbl = Gtk.Label('Agency: ')
        self.pack_start(self.lbl, False, False, 0)

        # our choices
        self.choice = Gtk.ComboBoxText.new()
        self.pack_start(self.choice, True, True, 5)

        # an add button
        add_btn = Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
        add_btn.connect('clicked', self.on_add_agency)
        self.pack_start(add_btn, False, False, 5)

        # add our agencies
        for agency in libsubte.Agency.agencies:
            #!mwd - we shouldn't be referencing by name 
            #  but by id, just incase we have two with the 
            #  same name
            self.choice.append_text(agency.name)
        self.choice.set_active(0)

    def get_label(self):
        return self.lbl

    def get_selection(self):
        selection = self.choice.get_active_text()
        for agency in libsubte.Agency.agencies:
            if agency.name == selection:
                return agency
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

    def on_add_agency(self, btn, user_data = None):
        # !mwd - we need a parent window
        dlg = AddAgencyDialog(None)
        dlg.show_all()

        if dlg.run() == Gtk.ResponseType.ACCEPT:
            # create a new agency
            a = libsubte.Agency(name = dlg.content.name)
            # if ok, refresh the combo box
            self.choice.append_text(a.name)

            index = len(self.choice.get_model())

            # set to the new item
            self.choice.set_active(index-1)

        dlg.destroy()

