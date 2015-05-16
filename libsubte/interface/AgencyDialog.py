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
from Locale import _

class AddAgencyDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, _('Add Agency'), parent,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            (_('Add'), Gtk.ResponseType.ACCEPT,
                             _('Cancel'), Gtk.ResponseType.CANCEL))

        self.content = AddAgency()
        self.get_content_area().add(self.content)

class EditAgencyDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, _('Edit Agency'), parent,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            (_('Edit'), Gtk.ResponseType.ACCEPT,
                             _('Cancel'), Gtk.ResponseType.CANCEL))

        self.content = AddAgency()
        self.get_content_area().add(self.content)

class AddAgency(Gtk.VBox):
    '''A vbox for adding an agency'''
    def __init__(self):
        Gtk.VBox.__init__(self, False)

        size_group = Gtk.SizeGroup(mode = Gtk.SizeGroupMode.HORIZONTAL)

        # name
        name_hbox = Gtk.HBox(False)
        name_lbl = Gtk.Label(_('Name: '))
        name_lbl.set_tooltip_text(_('Full name of the agency'))
        size_group.add_widget(name_lbl)       
        name_hbox.pack_start(name_lbl, False, False, 0)
        self.name_txt = Gtk.Entry()
        self.name_txt.set_tooltip_text(_('Full name of the agency'))
        name_hbox.pack_start(self.name_txt, True, True, 5)
        self.pack_start(name_hbox, True, True, 5)

        # url
        url_hbox = Gtk.HBox(False)
        url_lbl = Gtk.Label(_('URL: '))
        url_lbl.set_tooltip_text(_('Must begin with http:// or https://'))
        size_group.add_widget(url_lbl)       
        url_hbox.pack_start(url_lbl, False, False, 0)
        self.url_txt = Gtk.Entry()
        self.url_txt.set_tooltip_text(_('Must begin with http:// or https://'))
        url_hbox.pack_start(self.url_txt, True, True, 5)
        self.pack_start(url_hbox, True, True, 5)

        # timezone
        timezone_hbox = Gtk.HBox(False)
        timezone_lbl = Gtk.Label(_('Timezone: '))
        size_group.add_widget(timezone_lbl)       
        timezone_hbox.pack_start(timezone_lbl, False, False, 0)
        self.timezone_combo = Gtk.ComboBoxText.new()
        self.timezone_combo.append_text('America/Chicago')
        self.timezone_combo.append_text('Europe/Warsaw')
        timezone_hbox.pack_start(self.timezone_combo, True, True, 5)
        self.pack_start(timezone_hbox, True, True, 5)

        # language
        language_hbox = Gtk.HBox(False)
        language_lbl = Gtk.Label(_('Language: '))
        size_group.add_widget(language_lbl)       
        language_hbox.pack_start(language_lbl, False, False, 0)
        self.language_combo = Gtk.ComboBoxText.new()
        self.language_combo.append_text('EN')
        self.language_combo.append_text('PL')
        language_hbox.pack_start(self.language_combo, True, True, 5)
        self.pack_start(language_hbox, True, True, 5)

        # phone
        phone_hbox = Gtk.HBox(False)
        phone_lbl = Gtk.Label(_('Phone: '))
        size_group.add_widget(phone_lbl)       
        phone_hbox.pack_start(phone_lbl, False, False, 0)
        self.phone_txt = Gtk.Entry()
        phone_hbox.pack_start(self.phone_txt, True, True, 5)
        self.pack_start(phone_hbox, True, True, 5)

        # fare url
        fare_hbox = Gtk.HBox(False)
        fare_url_lbl = Gtk.Label(_('Fare URL: '))
        fare_url_lbl.set_tooltip_text(_('Must begin with http:// or https://'))
        size_group.add_widget(fare_url_lbl)       
        fare_hbox.pack_start(fare_url_lbl, False, False, 0)
        self.fare_url_txt = Gtk.Entry()
        self.fare_url_txt.set_tooltip_text(_('Must begin with http:// or https://'))
        fare_hbox.pack_start(self.fare_url_txt, True, True, 5)
        self.pack_start(fare_hbox, True, True, 5)

    name = property(lambda x: x.name_txt.get_text(), None)
    url = property(lambda x: x.url_txt.get_text(), None)
    timezone = property(lambda x: x.timezone_combo.get_active_text(), None)
    language = property(lambda x: x.language_combo.get_active_text(), None)
    phone = property(lambda x: x.phone_txt.get_text(), None)
    fare_url = property(lambda x: x.fare_url_txt.get_text(), None)


    def _fill(self, agency):
        if agency is None:
            return

        self.name_txt.set_text(agency.name)
        self.url_txt.set_text(agency.url)

        model = self.timezone_combo.get_model()
        it = model.get_iter_first()
        while it:
            if model.get_value(it, 0) == agency.timezone:
                self.timezone_combo.set_active_iter(it)
                break
            it = model.iter_next(it)
        if not it:
            self.timezone_combo.append_text(agency.timezone)

        model = self.language_combo.get_model()
        it = model.get_iter_first()
        while it:
            if model.get_value(it, 0) == agency.language.upper():
                self.language_combo.set_active_iter(it)
                break
            it = model.iter_next(it)
        if not it:
            self.language_combo.append_text(agency.language.upper())

        self.phone_txt.set_text(agency.phone)
        self.fare_url_txt.set_text(agency.fare_url)


class AgencyChoice(Gtk.HBox):
    def __init__(self):
        Gtk.HBox.__init__(self, False)

        self.lbl = Gtk.Label(_('Agency: '))
        self.pack_start(self.lbl, False, False, 0)

        # our choices
        self.choice = Gtk.ComboBoxText.new()
        self.pack_start(self.choice, True, True, 5)

        # an add button
        add_btn = Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
        add_btn.connect('clicked', self.on_add_agency)
        self.pack_start(add_btn, False, False, 5)

        # a modify button
        edit_btn = Gtk.Button.new_from_stock(Gtk.STOCK_EDIT)
        edit_btn.connect('clicked', self.on_edit_agency)
        self.pack_start(edit_btn, False, False, 5)

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

    def on_edit_agency(self, btn, user_data = None):
        agency = self.get_selection()
        if agency is None:
            return True

        # !mwd - we need a parent window
        dlg = EditAgencyDialog(None)
        dlg.content._fill(agency)
        dlg.show_all()

        if dlg.run() == Gtk.ResponseType.ACCEPT:
            ind = self.choice.get_active()
            self.choice.remove(ind)
            self.choice.insert_text(ind, dlg.content.name)
            self.choice.set_active(ind)
            agency.name = dlg.content.name
            agency.url = dlg.content.url
            agency.timezone = dlg.content.timezone
            agency.language = dlg.content.language
            agency.phone = dlg.content.phone
            agency.fare_url = dlg.content.fare_url

        dlg.destroy()

        return True
