import gtbuilder.interface as interface

from gi.repository import Gtk

if __name__ == '__main__':
    win = interface.GTGui()
    win.show_all()

    Gtk.main()
