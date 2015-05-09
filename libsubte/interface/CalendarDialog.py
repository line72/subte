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
from datetime import datetime
from dateutil.relativedelta import relativedelta

import libsubte
from libsubte import TripRoute
from libsubte import Trip

def yyyymmdd(s):
    if len(s) >= len('yyyy-mm-dd'):
        if (s[4] == '-' and s[7] == '-') or (s[4] == '.' and s[7] == '.') or (s[4] == ' ' and s[7] == ' ') or (s[4] == '/' and s[7] == '/'):
            return (s[0:4] + s[5:7] + s[8:10])
        else:
            return s[0:8]
    else:
        return s

class AddCalendarDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, 'Add Calendar', parent,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            ('Add', Gtk.ResponseType.ACCEPT,
                             'Cancel', Gtk.ResponseType.CANCEL))

        self.content = AddCalendar()
        self.get_content_area().add(self.content)

class EditCalendarDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, 'Edit Calendar', parent,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            ('Edit', Gtk.ResponseType.ACCEPT,
                             'Cancel', Gtk.ResponseType.CANCEL))

        self.content = AddCalendar()
        self.get_content_area().add(self.content)

class AddCalendar(Gtk.VBox):
    '''A vbox for adding an calendar'''
    def __init__(self):
        Gtk.VBox.__init__(self, False)

        size_group = Gtk.SizeGroup(mode = Gtk.SizeGroupMode.HORIZONTAL)

        # name
        namebox = Gtk.HBox(False)
        name_lbl = Gtk.Label('Name: ')
        size_group.add_widget(name_lbl)       
        namebox.pack_start(name_lbl, False, False, 0)
        self.name_txt = Gtk.Entry()
        namebox.pack_start(self.name_txt, True, True, 5)
        self.pack_start(namebox, True, True, 5)

        # days
        weekbox = Gtk.HBox(True)
        self.monday = Gtk.CheckButton('Monday')
        self.monday.set_active(True)
        weekbox.pack_start(self.monday, False, False, 0)
        self.tuesday = Gtk.CheckButton('Tuesday')
        self.tuesday.set_active(True)
        weekbox.pack_start(self.tuesday, False, False, 0)
        self.wednesday = Gtk.CheckButton('Wednesday')
        self.wednesday.set_active(True)
        weekbox.pack_start(self.wednesday, False, False, 0)
        self.thursday = Gtk.CheckButton('Thursday')
        self.thursday.set_active(True)
        weekbox.pack_start(self.thursday, False, False, 0)
        self.friday = Gtk.CheckButton('Friday')
        self.friday.set_active(True)
        weekbox.pack_start(self.friday, False, False, 0)
        self.saturday = Gtk.CheckButton('Saturday')
        self.saturday.set_active(True)
        weekbox.pack_start(self.saturday, False, False, 0)
        self.sunday = Gtk.CheckButton('Sunday')
        self.sunday.set_active(True)
        weekbox.pack_start(self.sunday, False, False, 0)
        self.pack_start(weekbox, True, True, 5)

        #!lukstafi - TODO: perhaps on-demand dialog with two calendars?
        # start date and end date
        datebox = Gtk.HBox(False)
        start_date_lbl = Gtk.Label('Start date: ')
        datebox.pack_start(start_date_lbl, False, False, 0)
        self.start_date_txt = Gtk.Entry()
        self.start_date_txt.set_text(yyyymmdd(datetime.now().isoformat()))
        datebox.pack_start(self.start_date_txt, True, True, 5)
        end_date_lbl = Gtk.Label('End date: ')
        datebox.pack_start(end_date_lbl, False, False, 0)
        self.end_date_txt = Gtk.Entry()
        self.end_date_txt.set_text(
            yyyymmdd((datetime.now() + relativedelta(years=+2)).isoformat()))
        datebox.pack_start(self.end_date_txt, True, True, 5)
        self.pack_start(datebox, True, True, 5)

        #!lukstafi - TODO: perhaps add nicer interface?
        # exceptions
        added_excnbox = Gtk.HBox(False)
        added_excn_lbl = Gtk.Label('Added days: ')
        added_excnbox.pack_start(added_excn_lbl, False, False, 0)
        self.added_excn_txt = Gtk.Entry()
        added_excnbox.pack_start(self.added_excn_txt, True, True, 5)
        self.pack_start(added_excnbox, True, True, 5)

        remov_excnbox = Gtk.HBox(False)
        remov_excn_lbl = Gtk.Label('Removed days: ')
        remov_excnbox.pack_start(remov_excn_lbl, False, False, 0)
        self.remov_excn_txt = Gtk.Entry()
        remov_excnbox.pack_start(self.remov_excn_txt, True, True, 5)
        self.pack_start(remov_excnbox, True, True, 5)

    def _fill(self, calendar):
        if calendar is None:
            return

        self.name_txt.set_text(calendar.name)
        self.monday.set_active(calendar.days[0])
        self.tuesday.set_active(calendar.days[1])
        self.wednesday.set_active(calendar.days[2])
        self.thursday.set_active(calendar.days[3])
        self.friday.set_active(calendar.days[4])
        self.saturday.set_active(calendar.days[5])
        self.sunday.set_active(calendar.days[6])
        self.start_date_txt.set_text(calendar.start_date)
        self.end_date_txt.set_text(calendar.end_date)
        self.added_excn_txt.set_text(" ".join(calendar.added_excn))
        self.remov_excn_txt.set_text(" ".join(calendar.remov_excn))

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

        # a modify button
        edit_btn = Gtk.Button.new_from_stock(Gtk.STOCK_EDIT)
        edit_btn.connect('clicked', self.on_edit_calendar)
        self.pack_start(edit_btn, False, False, 5)

        # a remove button
        rm_btn = Gtk.Button.new_from_stock(Gtk.STOCK_REMOVE)
        rm_btn.connect('clicked', self.on_rm_calendar)
        self.pack_start(rm_btn, False, False, 5)

        # add our calendars
        for calendar in libsubte.Calendar.calendars:
            #!mwd - we shouldn't be referencing by name 
            #  but by id, just incase we have two with the 
            #  same name
            self.choice.append_text(calendar.name)
        self.choice.set_active(0)

    def get_label(self):
        return self.lbl

    def get_selection_index(self):
        return self.choice.get_active()

    def get_selection(self):
        selection = self.choice.get_active_text()
        for calendar in libsubte.Calendar.calendars:
            if calendar.name == selection:
                return calendar
        return None

    def set_selection(self, calendar):
        if not calendar:
            return False

        model = self.choice.get_model()
        it = model.get_iter_first()
        while it:
            if model.get_value(it, 0) == calendar.name:
                self.choice.set_active_iter(it)
                return True
            it = model.iter_next(it)
        return False

    def on_add_calendar(self, btn, user_data = None):
        # !mwd - we need a parent window
        dlg = AddCalendarDialog(None)
        dlg.show_all()

        if dlg.run() == Gtk.ResponseType.ACCEPT:
            # create a new calendar
            a = libsubte.Calendar(service_name = dlg.content.name_txt.get_text(),
                                  monday = (1 if dlg.content.monday.get_active() else 0),
                                  tuesday = (1 if dlg.content.tuesday.get_active() else 0),
                                  wednesday = (1 if dlg.content.wednesday.get_active() else 0),
                                  thursday = (1 if dlg.content.thursday.get_active() else 0),
                                  friday = (1 if dlg.content.friday.get_active() else 0),
                                  saturday = (1 if dlg.content.saturday.get_active() else 0),
                                  sunday = (1 if dlg.content.sunday.get_active() else 0),
                                  start_date = dlg.content.start_date_txt.get_text(),
                                  end_date = dlg.content.end_date_txt.get_text(),
                                  added_excn = dlg.content.added_excn_txt.get_text().split(),
                                  remov_excn = dlg.content.remov_excn_txt.get_text().split())
            # if ok, refresh the combo box
            self.choice.append_text(a.name)

            index = len(self.choice.get_model())

            # set to the new item
            self.choice.set_active(index-1)

        dlg.destroy()

    def on_edit_calendar(self, btn, user_data = None):
        calendar = self.get_selection()
        if calendar is None:
            return True

        # !mwd - we need a parent window
        dlg = EditCalendarDialog(None)
        dlg.content._fill(calendar)
        dlg.show_all()

        if dlg.run() == Gtk.ResponseType.ACCEPT:
            # create a new calendar
            calendar.name = dlg.content.name_txt.get_text()
            calendar.days[0] = (1 if dlg.content.monday.get_active() else 0)
            calendar.days[1] = (1 if dlg.content.tuesday.get_active() else 0)
            calendar.days[2] = (1 if dlg.content.wednesday.get_active() else 0)
            calendar.days[3] = (1 if dlg.content.thursday.get_active() else 0)
            calendar.days[4] = (1 if dlg.content.friday.get_active() else 0)
            calendar.days[5] = (1 if dlg.content.saturday.get_active() else 0)
            calendar.days[6] = (1 if dlg.content.sunday.get_active() else 0)
            calendar.start_date = dlg.content.start_date_txt.get_text()
            calendar.end_date = dlg.content.end_date_txt.get_text()
            calendar.added_excn = dlg.content.added_excn_txt.get_text().split()
            calendar.remov_excn = dlg.content.remov_excn_txt.get_text().split()

        dlg.destroy()

        return True

    def on_rm_calendar(self, btn, user_data = None):
        calendar = self.get_selection()
        if calendar is None:
            return True

        dlg = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL,
                                Gtk.MessageType.WARNING,
                                Gtk.ButtonsType.OK_CANCEL,
                                "Delete this calendar?")
        resp = dlg.run()
        if resp == Gtk.ResponseType.OK:
            print 'deleting calendar', calendar
            index = self.get_selection_index()
            self.choice.remove(index)

            index = index - 1
            if index < 0: 
                index = 0
            self.choice.set_active(index)
            fallback_cal = self.get_selection()
            
            for tr_route in TripRoute.trip_routes:
                if tr_route.calendar == calendar:
                    tr_route.calendar = fallback_cal
            for tr in Trip.trips:
                if tr.calendar == calendar:
                    tr.calendar = fallback_cal
            calendar.destroy()

        dlg.destroy()

        return True
