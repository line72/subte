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

from multiprocessing import Process, Queue

import BaseHTTPServer
import socket

APIKEY = 'AIzaSyCA50HzNvL8vBSKGkb5OBzKF-qPutxixWo'


class GTServer(object):
    def __init__(self):
        self._queue = Queue()

        self._process = Process(target = build_server, args = (self._queue,))
        self._process.start()

    def stop(self):
        self._queue.put(True)
        self._process.join()

# Code taken from
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/425210/index_txt
class GTHTTPServer(BaseHTTPServer.HTTPServer):
    '''This is a simple web server that the client uses to show 
    google maps.'''
    def __init__(self, server_address, RequestHandlerClass, queue):
        BaseHTTPServer.HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self._queue = queue

    def server_bind(self):
        BaseHTTPServer.HTTPServer.server_bind(self)
        self.socket.settimeout(1)
        self._run = True

    def get_request(self):
        while self._run:
            try:
                sock, addr = self.socket.accept()
                sock.settimeout(None)
                return (sock, addr)
            except socket.timeout:
                pass

    def stop(self):
        self._run = False

    def serve(self):
        while self._run:
            try:
                r = self._queue.get(False)

                if r:
                    self.stop()
            except Exception, e: # should only handle queue.Empty
                pass

            self.handle_request()

class GTRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        f = open('gtbuilder/interface/index.html')
        content = f.read()
        f.close()

        content = content.replace('@APIKEY@', APIKEY)

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

def build_server(queue):
    server = GTHTTPServer(server_address = ('', 9876),
                          RequestHandlerClass = GTRequestHandler,
                          queue = queue)
    server.serve()
