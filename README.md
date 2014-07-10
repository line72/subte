Subte is an application to manage public transit data. It can create stops, build routes and timetables, and export to GTFS (General Transit Feed Specification) data which can be used by Google Transit, Open Trip Planner, and others.

This software was developed by Marcus Dillavou <line72@line72.net> (http://line72.net) to aid in building transite data for the BJCTA [Birmingham-Jefferson County Transit Authority] (http://www.bjcta.org) in Birmingham, AL. For more information, please see the project website:

http://line72.net/index.php/software/subte/

This software is licensed under the GPLv3 or later.

== Dependencies ==

python2.7
gobject-introspection
glib (with gobject introspection)
gtk3 (with gobject introspection)
clutter (with gobject introspection)
clutter-gtk (with gobject introspection)
libchamplain (with gobject introspection)
libchamplain-gtk (with gobject introspection)
python-exif
PIL or python-pillow
python-lxml
python-dateutil

== Building Under Linux ==

On Fedora Linux, you will need to install the following packages with yum

$ yum install gobject-introspection libchamplain-gtk python-exif python-pillo python-lxml python-dateutil clutter-gtk

You can then run directly:

$ ./subte

or you can install

$ python setup.py build
$ python setup.py install
$ subte

== Building Under Mac OSX ==

I have successfully run this under OSX using macports. You will need to install all the dependencies listed above. This requires having X (http://xquartz.macosforge.org/landing/) installed

== Building Under Windows ==

Install python2.7 from python.org

You can install almost all the required dependencies by installing the latest version of this package:
http://opensourcepack.blogspot.com/p/pygobject-pygi-aio.html

Any additional python dependencies (python-exif, python-pillow, python-lxml, python-dateutil) can be installed using pip (https://pypi.python.org/pypi/pip/) or easy_install (http://peak.telecommunity.com/DevCenter/EasyInstall)

Under windows, there is a bug with the map widget (libchamplain) that is causing events to not be handled correctly. This causes issues when clicking on the map and invalid coordinates being sent making subte almost useless. We are still investigating this.