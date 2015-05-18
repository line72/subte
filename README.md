Subte is an application to manage public transit data. It can create stops, build routes and timetables, and export to GTFS (General Transit Feed Specification) data which can be used by Google Transit, Open Trip Planner, and others.

This software was developed by Marcus Dillavou <line72@line72.net> (http://line72.net) to aid in building transite data for the BJCTA [Birmingham-Jefferson County Transit Authority] (http://www.bjcta.org) in Birmingham, AL. For more information, please see the project website:

http://line72.net/index.php/software/subte/

The software was enhanced by Lukasz Stafiniak <lukstafi@gmail.com> with:
* minor changes that appear to improve reliability (the program did not work out of the box for Lukasz),
* a dialog to edit transit agency data,
* export of KML and JSON / Javascript files with transit data, and `utils/display_map.html`, `utils/display_map.js` files, that together form a minimalistic Google Maps based web application to access bus timetables,
* a translation of the interface into Polish, the localization is determined by system settings.

This software is licensed under the GPLv3 or later.

## Usage

Hover the mouse pointer over a GUI element to see its description in the tooltip. To enter new times in the ''Trips'' or ''Frequencies'' tables: click on the `Add` button, double-click (or click) on the cell corresponding to a stop until an edit field appears, enter the departure time in the HH:MM or HH:MM:SS format, press `enter`. The times should always increase along a route, using `24:05` for five minutes after midnight on next day of the trip, `25:00` for 1 AM of the next day, etc. Before clicking on a stop, you may need to click on the balloon of the previously clicked stop, to dismiss it.

To provide the minimalistic web-based timetables interface:
* export the transit data by clicking on the `Export To Google` button,
* move the files `doc.kml` and `doc.js` into the target web hosting directory,
* edit the files `utils/display_map.html`, `utils/display_map.js`: replace each occurrence of `https://ENTER YOUR URL HERE/` with the web-facing address,
* copy the files `utils/display_map.html`, `utils/display_map.js` into the target web hosting directory,
* the interface is now available at the web-facing address of `display_map.html`.

(The `doc.kml` file is cached by the browser, so you may need to rename it, also in `display_map.js`, or alternatively clear the cache, for testing during development.)

To provide data to the Google Transit service, package the exported files with the `.txt` extension as a `.zip` archive and follow the instructions in [Google Transit Partner Program](https://maps.google.com/help/maps/mapcontent/transit/participate.html). But this requires authorization from the transit agencies.

The data can also be used with [Open Trip Planner](http://www.opentripplanner.org/) appliations, for example [OpenTripPlanner for Android](https://github.com/CUTR-at-USF/OpenTripPlanner-for-Android/wiki). But that requires setting up and maintaining an Open Trip Planner server. See [Birmingham, AL's public transit](http://line72.net//index.php?cID=130) for a "case study".

## Dependencies

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

## Building Under Linux

On Fedora Linux, you will need to install the following packages with yum

$ yum install gobject-introspection libchamplain-gtk python-exif python-pillo python-lxml python-dateutil clutter-gtk

On Ubuntu Linux:

$ sudo apt-get install gobject-introspection libchamplain-gtk-0.12-0 python-exif python-pil python-lxml python-dateutil libclutter-gtk-1.0-0

You can then run directly:

$ ./subte

or you can install

$ python setup.py build
$ python setup.py install
$ subte

## Building Under Mac OSX

I have successfully run this under OSX using macports. You will need to install all the dependencies listed above. This requires having X (http://xquartz.macosforge.org/landing/) installed

## Building Under Windows

Install python2.7 from python.org

You can install almost all the required dependencies by installing the latest version of this package:
http://opensourcepack.blogspot.com/p/pygobject-pygi-aio.html

Any additional python dependencies (python-exif, python-pillow, python-lxml, python-dateutil) can be installed using pip (https://pypi.python.org/pypi/pip/) or easy_install (http://peak.telecommunity.com/DevCenter/EasyInstall)

Under windows, there is a bug with the map widget (libchamplain) that is causing events to not be handled correctly. This causes issues when clicking on the map and invalid coordinates being sent making subte almost useless. We are still investigating this.