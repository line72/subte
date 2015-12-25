Subte is an application to manage public transit data. It can create stops, build routes and timetables, and export to GTFS (General Transit Feed Specification) data which can be used by Google Transit, Open Trip Planner, and others.

This software was developed by Marcus Dillavou <line72@line72.net> (http://line72.net) to aid in building transite data for the BJCTA [Birmingham-Jefferson County Transit Authority] (http://www.bjcta.org) in Birmingham, AL. For more information, please see the project website:

http://line72.net/index.php/software/subte/

The software was enhanced by Lukasz Stafiniak <lukstafi@gmail.com> with:
* minor changes that appear to improve reliability (the program did not work out of the box for Lukasz),
* a dialog to edit transit agency data,
* export of KML and JSON / Javascript files with transit data, and `utils/display_map.html/js`, `utils/display_stop.js`, `utils/display_route.html/js` files, that together form a minimalistic Google Maps based web application to access bus timetables,
* a translation of the interface into Polish, the localization is determined by system settings.

This software is licensed under the GPLv3 or later.

## Usage

Hover the mouse pointer over a GUI element to see its description in the tooltip. To enter new times in the ''Trips'' or ''Frequencies'' tables: click on the `Add` button, double-click (or click) on the cell corresponding to a stop until an edit field appears, enter the departure time in the HH:MM or HH:MM:SS format, press `enter`. The times should always increase along a route, using `24:05` for five minutes after midnight on next day of the trip, `25:00` for 1 AM of the next day, etc. Before clicking on a stop, you may need to click on the balloon of the previously clicked stop, to dismiss it.

Remember to fill all pull-down option lists before adding a new entity like a trip route (a group of trips) or a bus stop. If some pull-down list is empty, you need to create a new entry for it by clicking the `Add` button to the right. See the comments on required fields below.

Terminology:
* A ''calendar'' provides the days of bus trips, i.e. on which days exactly does a bus trip go.
* A ''route'' (despite the name) provides the agency and the calendar (i.e. the days of operation), of bus trips.
* A ''group of trips'' provides the stops and the hours of bus trips (and the information above, by selecting the route and the calendar).

Unfortunately, if a trip is going at an hour except on some specific days, or in addition on some specific days etc., you need to create a new calendar and a new group of trips just for this hour and for other hours sharing this exact exception, i.e. available at the exact same days.

The intended meaning of the fields corresponds to the GTFS specification:
[General Transit Feed Specification Reference](https://developers.google.com/transit/gtfs/reference).
However, for the purposes of the minimalistic web-based interface mentioned below, only the following fields are required:
* Either the name (preferred) or the description of a stop.
* The location of a stop (which you can enter by clicking on the map while the `Add stop` window is open).
* The route of a group of trips (click the `Add` button to the right of the pulldown menu if the group of trips needs a new route).
* The calendar of a group of trips (click the `Add` button to the right of the pulldown menu if the group of trips needs a new calendar).
* All the fields in a calendar except the start and expiry date:
** name of the calendar,
** days of operation,
** additional specific days if any,
** specific excluded days if any.
* The trip departure times under the button to the right of `Edit Trips:` (the trip frequencies, as in the button below, are not supported by the minimalistic web interface);
** note: first add the stops of the group of trips, also the `Edit trips` window might need expanding.
* Either the short name or the long name of a route.
* The agency of a route (click the `Add` button to the right of the pulldown menu if the route needs a new agency).
* The name of the agency.

The following fields are currently ignored by the minimalistic web interface:
* the name of a group of trips,
* the headsign of a group of trips,
* the frequencies of a group of trips,
* start and expiry dates of a calendar,
* information about agencies other than their name.

Remember to add the destination stop of a trip. The time of the destination stop is the arrival at destination time. Destination stops are not shown by some "windows" of the minimalistic web interface. The last stop of a trip is always assumed to be the destination stop.

To provide the minimalistic web-based timetables interface:
* export the transit data by clicking either on the `Export to KML with tables` toolbox button or the `Export to KML with links` toolbox button and selecting an empty directory,
* move all the files generated in the directory above into the target web hosting directory,
* copy the files `utils/display_map.html`, `utils/display_map.js`, `utils/display_route.html`, `utils/display_route.js` and `utils/display_stop.js` into the target web hosting directory,
* the interface is now available at the web-facing address of `display_map.html`.

(The `doc.kml` file is cached by the browser, so you may need to rename it, also in `display_map.js`, or alternatively clear the cache, for testing during development.)

To provide data to the Google Transit service, click on the `Export to GTFS` toolbox button, package the exported files with the `.txt` extension as a `.zip` archive and follow the instructions in [Google Transit Partner Program](https://maps.google.com/help/maps/mapcontent/transit/participate.html). But this requires authorization from the transit agencies.

The data can also be used with [Open Trip Planner](http://www.opentripplanner.org/) appliations, for example [OpenTripPlanner for Android](https://github.com/CUTR-at-USF/OpenTripPlanner-for-Android/wiki). But that requires setting up and maintaining an Open Trip Planner server. See [Birmingham, AL's public transit](http://line72.net//index.php?cID=130) for a "case study".

## Building Under Linux

Download and unpack the sources: e.g. click on the `Download ZIP` button on [https://github.com/lukstafi/subte](https://github.com/lukstafi/subte) and unpack the archive. Enter the directory, e.g.:

```
$ cd subte-master
```

On Fedora Linux, you will need to install the following packages with yum

```
$ yum install gobject-introspection libchamplain-gtk python-exif \
 python-pillo python-lxml python-dateutil clutter-gtk
```

On Ubuntu Linux:

```
$ sudo apt-get install gobject-introspection libchamplain-gtk-0.12-0 \
 python-exif python-pil python-lxml python-dateutil \
 libclutter-gtk-1.0-0 gir1.2-gtkclutter-1.0 gir1.2-champlain-0.12 \
 gir1.2-gtk-3.0 gir1.2-gtkchamplain-0.12
```

You can then run directly:

```
$ ./subte
```

or you can install

```
$ python setup.py build
$ python setup.py install
$ subte
```

## Building Under Mac OSX

I have successfully run this under OSX using macports. You will need to install all the dependencies listed above. This requires having X (http://xquartz.macosforge.org/landing/) installed

## Building Under Windows

Install python2.7 from python.org

You can install almost all the required dependencies by installing the latest version of this package:
http://opensourcepack.blogspot.com/p/pygobject-pygi-aio.html

Any additional python dependencies (python-exif, python-pillow, python-lxml, python-dateutil) can be installed using pip (https://pypi.python.org/pypi/pip/) or easy_install (http://peak.telecommunity.com/DevCenter/EasyInstall)

Under windows, there is a bug with the map widget (libchamplain) that is causing events to not be handled correctly. This causes issues when clicking on the map and invalid coordinates being sent making subte almost useless. We are still investigating this.

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
