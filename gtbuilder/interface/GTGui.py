
from gi.repository import Gtk

class GTGui(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = 'Google Transit Builder')
        self.connect('delete-event', self.on_quit)

    def on_quit(self, widget, evt, data = None):
        Gtk.main_quit()

