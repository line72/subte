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

import weakref
import md5
import os
import sys
try:
    import EXIF
except ImportError, e:
    import exifread as EXIF
try:
    import Image
except ImportError, e: # try Pillow support
    from PIL import Image

class Picture(object):
    pictures = []
    picture_id = 0

    def __init__(self, img, stop = None, latitude = None, longitude = None, orientation = 0):
        self.picture_id = Picture.new_id()
        self._stop = None

        self._img = img
        self.stop = stop

        self.orientation = orientation
        self._latitude = latitude
        self._longitude = longitude

        self.md5sum = None
        self.thumbnail = None

        try:
            f = open(img, 'rb')
            self.md5sum = md5.md5(f.read()).hexdigest()
            f.seek(0)

            # see if a thumbnail exists
            cache_dir = os.path.join(os.path.expanduser('~'), '.cache', 'subte')
            try: os.makedirs(cache_dir)
            except OSError: pass

            self.thumbnail = os.path.join(cache_dir, self.md5sum)
            try:
                f2 = open(self.thumbnail, 'rb')
                f2.close()
            except IOError, e:
                # no thumbnail cached, create one

                # see if the picture includes one
                f.seek(0) # reset f
                tags = EXIF.process_file(f, details = False)
                t = tags.get('JPEGThumbnail', None)
                if t:
                    # write this
                    f2 = open(self.thumbnail, 'wb')
                    f2.write(t)
                    f2.close()
                else:
                    # no embeded thumbnail, generate one?
                    im = Image.open(f)
                    im.thumbnail((128, 128))
                    im.save(self.thumbnail, 'JPEG')
        except IOError, e:
            pass

        self.ignored = False

        if self._latitude is None or self._longitude is None:
            self._load_gps_coords()

        # add us
        Picture.pictures.append(self)

    image = property(lambda x: x._img, None)
    stop_id = property(lambda x: x.stop.stop_id if x.stop else -1)

    def destroy(self):
        self.stop = None
        try:
            Picture.pictures.remove(self)
        except ValueError, e:
            pass

    @property
    def stop(self):
        if self._stop:
            return self._stop()
        return None
    @stop.setter
    def stop(self, s):
        if s:
            self._stop = weakref.ref(s)
        else:
            self._stop = None

    @property
    def latitude(self):
        if self.stop:
            return self.stop.latitude
        else:
            return self._latitude

    @property
    def longitude(self):
        if self.stop:
            return self.stop.longitude
        else:
            return self._longitude 

    def _load_gps_coords(self):
        # get the exif info
        try:
            f = open(self._img, 'rb')
            tags = EXIF.process_file(f, details=False)
            if len(tags) == 0:
                raise IOError("No EXIF tags")

            lat = tags.get('GPS GPSLatitude', None)
            lon = tags.get('GPS GPSLongitude', None)
            lat_ref = tags.get('GPS GPSLatitudeRef', 'N')
            lon_ref = tags.get('GPS GPSLongitudeRef', 'W')

            # convert to lat/long
            # from:
            # http://www.nihilogic.dk/labs/gps_exif_google_maps/

            i = -1 if lat_ref is 'N' else 1
            flat = ((lat.values[0].num / float(lat.values[0].den)) + \
                        ((lat.values[1].num / float(lat.values[1].den)) / 60.0) + \
                        ((lat.values[2].num /float(lat.values[2].den)) / 3600.0)) * i

            j = 1 if lon_ref is 'W' else -1
            flon = ((lon.values[0].num / float(lon.values[0].den)) + \
                        ((lon.values[1].num / float(lon.values[1].den)) / 60.0) + \
                        ((lon.values[2].num /float(lon.values[2].den)) / 3600.0)) * j

            self._latitude = flat
            self._longitude = flon

            # orientation
            orientation_tag = tags.get('Image Orientation', None)

            if orientation_tag is not None:
                orientation_v = orientation_tag.values

                if orientation_v[0] == 8: # counter clock wise
                    self.orientation = -90
                elif orientation_v[0] == 6: # clock wise
                    self.orientation = 90
                elif orientation_v[0] == 3: # 180
                    self.orientation = 180
            else:
                self.orientation = 0

        except (IOError, AttributeError), e:
            print >> sys.stderr, 'Error loading gps coords for %s:' % self._img, e
            self._latitude = 0
            self._longitude = 0
            self.orientation = 0
        

    @classmethod
    def is_duplicate(cls, md5sum):
        for picture in cls.pictures:
            if md5sum == picture.md5sum:
                return True

        return False
            
    @classmethod
    def get(cls, picture_id):
        for picture in cls.pictures:
            if picture.picture_id == picture_id:
                return picture
        return None

    @classmethod
    def new_id(cls):
        while True:
            cls.picture_id += 1
            if cls.picture_id not in [x.picture_id for x in Picture.pictures]:
                return cls.picture_id

