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

function initialize() {
  var src = document.URL.substr(0,document.URL.lastIndexOf('/')) + '/doc.kml';
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

function showStopRoute(s_id, r_id) {
    var sidebar = document.getElementById('cur-timetable');
    buildStopRouteTbl(s_id, r_id, new Date(), sidebar);
}

function buildTimetable(name, date, disp) {
    var tomorrow = new Date();
    tomorrow.setDate(date.getDate() + 1);
    var bus_tbl;
    var name_tbl;
    var id;
    if (name in stop_js_id) {
        name_tbl = route_names;
        id = stop_js_id[name];
        bus_tbl = stop_route_tables[id];
    } else if (name in route_js_id) {
        bus_tbl = {};
        id = route_js_id[name];
        name_tbl = stop_names;
        // skipping the destination stop
        for (var i = 0; i < route_stops[id].length - 1; i++) {
            var s_id = route_stops[id][i];
            bus_tbl[s_id] = stop_route_tables[s_id][id];
        }
    } else {
        disp.innerHtml =
            msg1 + showTime(date.toLocaleString());
        return;
    }
    disp.innerHTML = ""
    var header1 = document.createElement('h2');
    header1.appendChild(document.createTextNode(name + ": " + msg7));
    disp.appendChild(header1);
    disp.appendChild(document.createTextNode(
        msg2 + date.toLocaleDateString() +
            msg3 + showTime(date.toLocaleTimeString()) + '.'));
    for (i in bus_tbl) { // route or stop
        var sub_tbl = bus_tbl[i];
        var empty_case = true;
        for (cal in sub_tbl) {
            if (!dayInCalendar(date, calendars[cal])) {
                continue;
            }
            var times = sub_tbl[cal];
            for (j in times) {
                if (timeAfter (times[j], date)) {
                    empty_case = false;
                }
            }
        }
        if (empty_case) continue;
        var subname = name_tbl[i];
        var subheader = document.createElement('h3');
        subheader.appendChild(document.createTextNode(subname));
        disp.appendChild(subheader);
        for (cal in sub_tbl) {
            if (!dayInCalendar(date, calendars[cal])) {
                continue;
            }
            var times = sub_tbl[cal];
            for (j in times) {
                if (timeAfter (times[j], date)) {
                    disp.appendChild(
                        document.createTextNode(showTime(times[j]) + ' '));
                }
            }
        }
    }
    var header2 = document.createElement('h2');
    header2.appendChild(document.createTextNode(name + ": " + msg8));
    disp.appendChild(header2);
    disp.appendChild(document.createTextNode(
        msg2 + tomorrow.toLocaleDateString() + '.'));
    for (i in bus_tbl) { // route or stop
        var sub_tbl = bus_tbl[i];
        var empty_case = true;
        for (cal in sub_tbl) {
            if (dayInCalendar(tomorrow, calendars[cal]) &&
                sub_tbl[cal].length > 0) {
                empty_case = false;
            }
        }
        if (empty_case) continue;
        var subname = name_tbl[i];
        var subheader = document.createElement('h3');
        subheader.appendChild(document.createTextNode(subname));
        disp.appendChild(subheader);
        for (cal in sub_tbl) {
            if (!dayInCalendar(tomorrow, calendars[cal])) {
                continue;
            }
            var times = sub_tbl[cal];
            for (j in times) {
                disp.appendChild(
                    document.createTextNode(showTime(times[j]) + ' '));
            }
        }
    }
}


function buildStopRoute(s_id, r_id, date, disp) {
    var route_tbl = stop_route_tables[s_id][r_id];
    // disp.innerHTML =
    //     msg2 + date.toLocaleDateString() +
    //     msg3 + showTime(date.toLocaleTimeString()) + '.';
    var header = document.createElement('h3');
    var s_name = stop_names[s_id];
    var r_name = route_names[r_id];
    header.appendChild(document.createTextNode(s_name + ' - ' + r_name));
    disp.appendChild(header);
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
    var yyyymmdd = "" + d.getFullYear() +
        (d.getMonth() < 9 ? "0" : "") + (d.getMonth()+1) +
        (d.getDate() < 10 ? "0" : "") + d.getDate();
    if (cal['added_excn'].indexOf(yyyymmdd) > -1) {
        return true;
    }
    if (cal['remov_excn'].indexOf(yyyymmdd) > -1) {
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
