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

from gi.repository import Gtk, WebKit

class GTMap(WebKit.WebView):
    def __init__(self, key):
        WebKit.WebView.__init__(self)
        
        self.__key = key

        self.connect('load-finished', self.on_load_finished)

        # load an initial page
        self.load_uri('http://localhost:9876/%s' % key)
        #self.load_uri('http://www.google.com')

    def on_load_finished(self, view, frame):
        print 'finished loading'
        
        #print dir(self)

        # add a callback
        doc = self.get_dom_document()
        #print dir(doc)
        #print 'v=', doc.has_child_nodes()

        map_canvas = doc.get_element_by_id('map_canvas')
        map_canvas.connect_object('click-event', self.on_click, map_canvas)

        return True

    def on_click(self, p1, p2):
        print 'on_click', p1, p2

    
