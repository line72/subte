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


function initialize() {
    var route_id = gup('route', document.location.search);
    var stop_id = gup('stop', document.location.search);
    var agency_id = gup('agency', document.location.search);
    var route_n = route_names[route_id];
    var stop_n = stop_names[stop_id];
    var agency_n = agency_names[agency_id];
    var date = new Date();
    var tomorrow = new Date();
    tomorrow.setDate(date.getDate() + 1);
    var heading_doc = document.getElementById('routeheading');
    var timetable_doc = document.getElementById('timetable');
    var routelist_doc = document.getElementById('routelist');

    var headingtable = document.createElement('table');
    var h = document.createElement('tr');
    var d = document.createElement('td');
    d.appendChild(document.createTextNode(msg4));
    h.appendChild(d);
    d = document.createElement('td');
    d.appendChild(document.createTextNode(agency_n));    
    h.appendChild(d);
    headingtable.appendChild(h);
    h = document.createElement('tr');
    d = document.createElement('td');
    d.appendChild(document.createTextNode(msg5));
    h.appendChild(d);
    d = document.createElement('td');
    d.appendChild(document.createTextNode(stop_n));    
    h.appendChild(d);
    headingtable.appendChild(h);
    h = document.createElement('tr');
    d = document.createElement('td');
    d.appendChild(document.createTextNode(msg6));
    h.appendChild(d);
    d = document.createElement('td');
    d.appendChild(document.createTextNode(route_n));    
    h.appendChild(d);
    headingtable.appendChild(h);
    heading_doc.appendChild(headingtable);

    var timetable = document.createElement('table');
    var cals = document.createElement('tr');
    var tbl = stop_route_tables[stop_id][route_id];
    for (var i = 0; i < calendar_names.length; i++) {
        var cal_n = calendar_names[i];
        if (!(cal_n in tbl)) continue;
        var cal_h = document.createElement('th');
        cal_h.appendChild(document.createTextNode(cal_n));
        if (dayInCalendar (tomorrow, calendars[cal_n])) {
            cal_h.style.textDecoration = "underline";
        }
        cals.appendChild(cal_h);
    }
    timetable.appendChild(cals);
    cals = document.createElement('tr');
    for (var i = 0; i < calendar_names.length; i++) {
        var cal_n = calendar_names[i];
        if (!(cal_n in tbl)) continue;
        var cal_d = document.createElement('td');
        buildTimetable(cal_n, tbl[cal_n], date, cal_d);
        cals.appendChild(cal_d);
    }
    timetable.appendChild(cals);
    timetable_doc.appendChild(timetable);

    var routetable = document.createElement('table');
    var stops = route_stops[route_id];
    // Skip the destination stop -- it is not in the stop_route_tables
    for (var i = 0; i < stops.length - 1; i++) {
        stop_t = document.createElement('tr');
        stop = document.createElement('a');
        stop_name = document.createTextNode(stop_names[stops[i]]);
        stop.appendChild(stop_name);
        stop.href =
            'display_route.html?stop=' + stops[i] +
            '&route=' + route_id + '&agency=' + agency_id;
        if (stops[i] == stop_id) {
            stop.style.borderStyle = "groove";
        }
        stop_t.appendChild(stop);
        routetable.appendChild(stop_t);
    }
    routelist_doc.appendChild(routetable);
}

function buildTimetable (cal_n, cal_tbl, date, disp) {
    var table = document.createElement('table');
    var times = groupByHour(cal_tbl);
    var hours = Object.keys(times).sort();
    for (var i = 0; i < hours.length; i++) {
        var node = document.createElement('tr');
        var hour = document.createElement('td');
        hour.style.fontWeight = "bold";
        var h = hours[i];
        hour.appendChild(document.createTextNode(h));
        node.appendChild(hour);
        for (var j = 0; j < times[h].length; j++) {
            var minute = document.createElement('td');
            m = times[h][j];
            if (dayInCalendar (date, calendars[cal_n]) &&
                timeAfter (h + ":" + m, date)) {
                minute.style.textDecoration = "underline";
            }
            minute.appendChild(document.createTextNode(m));
            node.appendChild(minute);
        }
        table.appendChild(node);
    }
    disp.appendChild(table);
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

// With IDs, the preprocessing here is not really needed.
function gup(name, url) {
  if (!url) url = location.href;
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec( url );
  return results == null ? null :
           decodeURIComponent(results[1]).replace(/\+/," ");
}

function groupByHour(tbl) {
    var grouped = new Map();
    for (var i = 0; i < tbl.length; i++) {
        var v = tbl[i].split(':');
        var k = v[0];
        if (k.length == 1) k = "0" + k;
        if (!(k in grouped)) grouped[k] = new Array();
        grouped[k].push(v.slice(1, v.length));
    }
    return grouped;
}

window.addEventListener('load', initialize);
