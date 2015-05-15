//
// Copyright (C) 2015 - Lukasz Stafiniak
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 3, or (at your option)
// any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA.

var map;
var src = 'https://ENTER YOUR URL HERE/doc.kml';

function initialize() {
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    center: new google.maps.LatLng(-19.257753, 146.823688),
    zoom: 2,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });
  loadKmlLayer(src, map);
}

function loadKmlLayer(src, map) {
  var kmlLayer = new google.maps.KmlLayer(src, {
    suppressInfoWindows: false,
    preserveViewport: false,
    map: map
  });
  google.maps.event.addListener(kmlLayer, 'click', function(event) {
    var sidebar = document.getElementById('cur-timetable');
    buildTimetable(event.featureData.name, new Date(), sidebar);
  });
}

function buildTimetable(name, date, disp) {
    var bus_tbl;
    if (name in stop_tables) {
        bus_tbl = stop_tables[name];
    } else if (name in route_tables) {
        bus_tbl = route_tables[name];
    } else {
        disp.innerHtml =
            'Select a bus stop or a bus route. Time: ' +
            showTime(date.toLocaleString());
        return;
    }
    disp.innerHTML =
        'Showing times for day ' + date.toLocaleDateString() +
        ' after hour ' + showTime(date.toLocaleTimeString()) + '.';
    var header = document.createElement('h2');
    header.appendChild(document.createTextNode(name));
    disp.appendChild(header);
    for (route in bus_tbl) { // actually, route or stop
        var subheader = document.createElement('h3');
        subheader.appendChild(document.createTextNode(route));
        disp.appendChild(subheader);
        var route_tbl = bus_tbl[route];
        for (cal in route_tbl) {
            if (!dayInCalendar (date, calendars[cal])) {
                continue;
            }
            var times = route_tbl[cal];
            for (i in times) {
                if (timeAfter (times[i], date)) {
                    disp.appendChild(
                        document.createTextNode(showTime(times[i]) + ' '));
                }
            }
        }
    }
}

function showTime(t) {
    if (t[0] == '0') {
        t = t.substring(1, t.length);
    }
    if (t[t.length - 1] == '.' || t[t.length - 1] == 'm' ||
        t[t.length - 1] == 'M') {
        return t;
    }
    if (t[5] == ':') {
        return t.substring(0, 5);
    } else if (t[4] == ':') {
        return t.substring(0, 4);
    } else {
        return t;
    }
}

function dayInCalendar(d, cal) {
    var yymmdd = "" + d.getFullYear() +
        (d.getMonth() < 9 ? "0" : "") + (d.getMonth()+1) +
        (d.getDate() < 10 ? "0" : "") + d.getDate();
    if (cal['added_excn'].indexOf(yymmdd) > -1) {
        return true;
    }
    if (cal['remov_excn'].indexOf(yymmdd) > -1) {
        return false;
    }
    var day_no = d.getDay() == 0 ? 6 : d.getDay() - 1;
    return cal['days'][day_no] == 1;
}

function timeAfter(t, d) {
    // TODO: this is a bit of a hack, making assumptions about the formats.
    if (t[1] == ':') { // get the HH:MM:SS format
        t = "0" + t;
    }
    return t >= d.toLocaleTimeString();
}

google.maps.event.addDomListener(window, 'load', initialize);
