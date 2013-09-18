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

from lxml import etree

import libsubte

class KMLParser(object):
    def __init__(self):
        pass

    def parse(self, f):
        '''Parse a kml file and return all the paths'''
        paths = []

        tree = etree.parse(f)

        # go through each placemark
        for placemark in tree.getroot().iter('{*}Placemark'):
            name = placemark.findtext('{*}name')
            coords = []

            geom_node = placemark.find('{*}MultiGeometry')
            if geom_node is not None:
                line_str = geom_node.find('{*}LineString')
            else:
                line_str = placemark.find('{*}LineString')

            if line_str is not None:
                coord_str = line_str.findtext('{*}coordinates')
                if coord_str is not None:
                    x = coord_str.split(' ')
                    for k in x:
                        x2 = k.split(',')
                        if len(x2) == 2:
                            coords.append((float(x2[1]), float(x2[0])))
                        elif len(x2) == 3:
                            coords.append((float(x2[1]), float(x2[0])))

            if len(coords) > 0:
                path = libsubte.Path(name, coords)
                paths.append(path)

        return paths
