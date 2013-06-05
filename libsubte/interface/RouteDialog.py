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

from AgencyDialog import AgencyChoice

class AddRouteDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, 'Add Route', parent,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            ('Add', Gtk.ResponseType.ACCEPT,
                             'Cancel', Gtk.ResponseType.CANCEL))

        self.content = AddRoute()
        self.get_content_area().add(self.content)

class EditRouteDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, 'Edit Route', parent,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            ('Edit', Gtk.ResponseType.ACCEPT,
                             'Cancel', Gtk.ResponseType.CANCEL))

        self.content = AddRoute()
        self.get_content_area().add(self.content)


class AddRoute(Gtk.VBox):
    '''A vbox for adding an route'''
    def __init__(self):
        Gtk.VBox.__init__(self, False)

        size_group = Gtk.SizeGroup(mode = Gtk.SizeGroupMode.HORIZONTAL)


        # name
        hbox = Gtk.HBox(False)
        name_lbl = Gtk.Label('Short Name: ')
        size_group.add_widget(name_lbl)       
        hbox.pack_start(name_lbl, False, False, 0)
        self.name_txt = Gtk.Entry()
        hbox.pack_start(self.name_txt, True, True, 5)

        self.pack_start(hbox, True, False, 5)

        # name
        hbox = Gtk.HBox(False)
        name_lbl = Gtk.Label('Long Name: ')
        size_group.add_widget(name_lbl)       
        hbox.pack_start(name_lbl, False, False, 0)
        self.long_name_txt = Gtk.Entry()
        hbox.pack_start(self.long_name_txt, True, True, 5)

        self.pack_start(hbox, True, False, 5)


        # description
        hbox = Gtk.HBox(False)
        description_lbl = Gtk.Label('Description: ')
        size_group.add_widget(description_lbl)       
        hbox.pack_start(description_lbl, False, False, 0)
        self.description_txt = Gtk.TextView()
        hbox.pack_start(self.description_txt, True, True, 5)

        self.pack_start(hbox, True, True, 5)

        # agency
        self.agency_hbox = AgencyChoice()
        size_group.add_widget(self.agency_hbox.get_label())
        self.pack_start(self.agency_hbox, True, False, 5)

    def get_name(self):
        return self.name_txt.get_text()

    def get_long_name(self):
        return self.long_name_txt.get_text()

    def get_description(self):
        b = self.description_txt.get_buffer()
        return b.get_text(b.get_start_iter(), b.get_end_iter(), False)

    def set_description(self, desc):
        b = Gtk.TextBuffer()
        b.set_text(desc)
        self.description_txt.set_buffer(b)

    def get_agency(self):
        return self.agency_hbox.get_selection()

    def _fill(self, route):
        if route is None:
            return

        self.name_txt.set_text(route.short_name)
        self.long_name_txt.set_text(route.long_name)
        self.set_description(route.description)
        if route.agency:
            self.agency_hbox.set_selection(route.agency.name)


class RouteChoice(Gtk.HBox):
    def __init__(self):
        Gtk.HBox.__init__(self, False)

        self.lbl = Gtk.Label('Route: ')
        self.pack_start(self.lbl, False, False, 0)

        # our choices
        self.choice = Gtk.ComboBoxText.new()
        self.pack_start(self.choice, True, True, 5)

        # an add button
        add_btn = Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
        add_btn.connect('clicked', self.on_add_route)
        self.pack_start(add_btn, False, False, 5)

        # a modify button
        edit_btn = Gtk.Button.new_from_stock(Gtk.STOCK_EDIT)
        edit_btn.connect('clicked', self.on_edit_route)
        self.pack_start(edit_btn, False, False, 5)

        # a remove button
        rm_btn = Gtk.Button.new_from_stock(Gtk.STOCK_REMOVE)
        rm_btn.connect('clicked', self.on_rm_route)
        self.pack_start(rm_btn, False, False, 5)

        # add our agencies
        for route in libsubte.Route.routes:
            #!mwd - we shouldn't be referencing by name 
            #  but by id, just incase we have two with the 
            #  same name
            self.choice.append_text(route.short_name)
        self.choice.set_active(0)

    def get_label(self):
        return self.lbl

    def get_selection_index(self):
        return self.choice.get_active()

    def get_selection(self):
        selection = self.choice.get_active_text()
        for route in libsubte.Route.routes:
            if route.short_name == selection:
                return route
        return None

    def set_selection(self, v):
        if v is None:
            return False

        model = self.choice.get_model()
        it = model.get_iter_first()
        while it:
            if model.get_value(it, 0) == v.short_name:
                self.choice.set_active_iter(it)
                return True
            it = model.iter_next(it)
        return False

    def on_add_route(self, btn, user_data = None):
        # !mwd - we need a parent window
        dlg = AddRouteDialog(None)
        dlg.show_all()

        if dlg.run() == Gtk.ResponseType.ACCEPT:
            # create a new route
            name = dlg.content.get_name()
            long_name = dlg.content.get_long_name()
            description = dlg.content.get_description()
            agency = dlg.content.get_agency()

            a = libsubte.Route(agency, name, long_name, description)
            # if ok, refresh the combo box
            self.choice.append_text(a.short_name)

            index = len(self.choice.get_model())

            # set to the new item
            self.choice.set_active(index-1)

        dlg.destroy()

        return True

    def on_edit_route(self, btn, user_data = None):
        route = self.get_selection()
        if route is None:
            return True

        # !mwd - we need a parent window
        dlg = EditRouteDialog(None)
        dlg.content._fill(route)
        dlg.show_all()

        if dlg.run() == Gtk.ResponseType.ACCEPT:
            # create a new route
            route.short_name = dlg.content.get_name()
            route.long_name = dlg.content.get_long_name()
            route.description = dlg.content.get_description()
            route.agency = dlg.content.get_agency()

        dlg.destroy()

        return True

    def on_rm_route(self, btn, user_data = None):
        route = self.get_selection()
        if route is None:
            return True

        dlg = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL,
                                Gtk.MessageType.WARNING,
                                Gtk.ButtonsType.OK_CANCEL,
                                "Delete this route?")
        resp = dlg.run()
        if resp == Gtk.ResponseType.OK:
            print 'deleting route', route
            index = self.get_selection_index()
            self.choice.remove(index)

            index = index - 1
            if index < 0: 
                index = 0
            self.choice.set_active(index)
            
            route.destroy()

        dlg.destroy()

        return True
