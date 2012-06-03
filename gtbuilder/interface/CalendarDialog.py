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

import gtbuilder

class AddCalendarDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, 'Add Calendar', parent,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            ('Add', Gtk.ResponseType.ACCEPT,
                             'Cancel', Gtk.ResponseType.CANCEL))

        self.content = AddCalendar()
        self.get_content_area().add(self.content)

class AddCalendar(Gtk.VBox):
    '''A vbox for adding an calendar'''
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

        # days

        # start date

        # end date


    name = property(lambda x: x.name_txt.get_text(), None)


class CalendarChoice(Gtk.HBox):
    def __init__(self):
        Gtk.HBox.__init__(self, False)

        self.lbl = Gtk.Label('Calendar: ')
        self.pack_start(self.lbl, False, False, 0)

        # our choices
        self.choice = Gtk.ComboBoxText.new()
        self.pack_start(self.choice, True, True, 5)

        # an add button
        add_btn = Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
        add_btn.connect('clicked', self.on_add_calendar)
        self.pack_start(add_btn, False, False, 5)

        # add our calendars
        for calendar in gtbuilder.Calendar.calendars:
            #!mwd - we shouldn't be referencing by name 
            #  but by id, just incase we have two with the 
            #  same name
            self.choice.append_text(calendar.name)
        self.choice.set_active(0)

    def get_label(self):
        return self.lbl

    def get_selection(self):
        selection = self.choice.get_active_text()
        for calendar in gtbuilder.Calendar.calendars:
            if calendar.name == selection:
                return calendar
        return None

    def on_add_calendar(self, btn, user_data = None):
        # !mwd - we need a parent window
        dlg = AddCalendarDialog(None)
        dlg.show_all()

        if dlg.run() == Gtk.ResponseType.ACCEPT:
            # create a new calendar
            a = gtbuilder.Calendar(service_name = dlg.content.name)
            # if ok, refresh the combo box
            self.choice.append_text(a.name)

            index = len(self.choice.get_model())

            # set to the new item
            self.choice.set_active(index-1)

        dlg.destroy()

