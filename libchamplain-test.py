from gi.repository import GtkClutter, Clutter
GtkClutter.init([]) # must be initialized before importing the rest!

from gi.repository import GObject, Gtk, Champlain, GtkChamplain
import sys

def main():
    GObject.threads_init()

    win = Gtk.Window()
    win.connect('destroy', lambda x: Gtk.main_quit())

    vbox = Gtk.VBox(False, 12)

    #view = Champlain.View()
    #print 'view=', view
    #view.set_scroll_mode

    map_widget = GtkChamplain.Embed()
    map_widget.set_size_request(640, 480)

    view = map_widget.get_view()
    print 'view=', view, dir(view)
    view.set_size(640, 480)

    print 'map=', map_widget
    vbox.pack_start(map_widget, True, True, 0)
    #vbox.add(map_widget)
    #win.add(map_widget)

    btn = Gtk.Button(label = 'test')
    vbox.pack_start(btn, False, True, 0)

    win.add(vbox)


    win.show_all()

    Gtk.main()

main()
