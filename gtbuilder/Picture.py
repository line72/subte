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
import EXIF

class Picture(object):
    pictures = []
    picture_id = 0

    def __init__(self, img, stop = None):
        self.picture_id = Picture.new_id()
        self._stop = None

        self._img = img
        self.stop = stop

        self.md5sum = None
        self.thumbnail = None

        try:
            f = open(img, 'rb')
            self.md5sum = md5.md5(f.read()).hexdigest()

            # write out a thumbnail
            cache_dir = os.path.join(os.path.expanduser('~'), '.cache', 'gtbuilder')
            try: os.makedirs(cache_dir)
            except OSError: pass

            f.seek(0) # reset f
            tags = EXIF.process_file(f, details = False)
            t = tags.get('JPEGThumbnail', None)
            if t:
                thumb_md5 = md5.md5(t).hexdigest()

                self.thumbnail = os.path.join(cache_dir, thumb_md5)

                # write this
                try:
                    os.stat(self.thumbnail)
                except OSError, e: # doesn't exist, write it
                    f2 = open(self.thumbnail, 'wb')
                    f2.write(t)
                    f2.close()
            else:
                print >> sys.stderr, "Image %s has no thumbnail" % img
        except IOError, e:
            pass

        self.ignored = False

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

