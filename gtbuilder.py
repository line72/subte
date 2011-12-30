from gi.repository import GtkClutter, Clutter
GtkClutter.init([]) # this must be initialized before anything else!

import gtbuilder.interface as interface

from gi.repository import Gtk, GObject

if __name__ == '__main__':
    GObject.threads_init()

    win = interface.GTGui()
    win.show_all()

    Gtk.main()
