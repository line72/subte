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
    var calRow = document.createElement('tr');
    var data = stop_route_tables[stop_id][route_id];
    var calData = calColumnsFor(data);
    console.log('DEBUG: calData=', calData);
    for (var i = 0; i < calData.columns.length; i++) {
        var cal_c = calData.columns[i];
        var cal_n =
            cal_c.beg == cal_c.end ? dayAbbr[cal_c.beg] :
            dayAbbr[cal_c.beg] + '-' + dayAbbr[cal_c.end];
        var cal_h = document.createElement('th');
        cal_h.appendChild(document.createTextNode(cal_n));
        cal_c.calendarIds.forEach (function(cal) {
            if (dayInCalendar(tomorrow, calData.calIdToCalendar[cal])) {
                cal_h.style.textDecoration = "underline";
            }
        });
        calRow.appendChild(cal_h);
    }
    timetable.appendChild(calRow);
    var tblData = calData.columns.map(
        tblColumnFor.bind(undefined, data, calData.calIdToName));
    calRow = document.createElement('tr');
    for (var i = 0; i < calData.columns.length; i++) {
        var tbl_c = tblData[i];
        var cal_d = document.createElement('td');
        buildTimetable(tbl_c, calData.calIdToCalendar, date, cal_d);
        calRow.appendChild(cal_d);
    }
    timetable.appendChild(calRow);
    timetable_doc.appendChild(timetable);
    var legend = createCalLegend(calData.calIdToCalendar);
    if (legend) {
        timetable_doc.appendChild(legend);
    }

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

function calColumnsFor(data) {
    var calNames = Object.keys(data);
    var columns = [];
    var calIdToCalendar = {};
    var calIdToName = {};
    var calNameToId = {};

    for (var i = 0; i < calNames.length; i++) {
        var id = i + 1;
        var name = calNames[i];
        calNameToId[name] = id;
        calIdToCalendar[id] = calendars[name];
        calIdToName[id] = name;
    }
    var curColumn = null;
    for (var day = 0; day < 7; day++) {
        var dayCalIds = [];
        for (var i = 0; i < calNames.length; i++) {
            var cal = calendars[calNames[i]];
            if (cal.days[day]) {
                dayCalIds.push(i + 1);
            }
        }
        if (curColumn) {
            if (curColumn.calendarIds.join(' ') == dayCalIds.join(' ')) {
                curColumn.end = day;
            } else {
                columns.push(curColumn);
                curColumn = null;
            }
        }
        if (!curColumn && dayCalIds.length > 0) {
            curColumn = {beg: day, end: day, calendarIds: dayCalIds};
        }
    }
    if (curColumn) {
        columns.push(curColumn);
    }
    return {columns: columns,
            calIdToCalendar: calIdToCalendar,
            calIdToName: calIdToName,
            calNameToId: calNameToId};
}

function tblColumnFor(data, calIdToName, calColumn) {
    var times = [];
    calColumn.calendarIds.forEach(function (calId) {
        var courses = data[calIdToName[calId]];
        if (courses) {
            courses.forEach(function (time) {
                if (time) {
                    times.push({time: time, calId: calId});
                }
            });
        }});
    return times;
}

function buildTimetable (tbl_c, calIdToCalendar, date, disp) {
    var table = document.createElement('table');
    var times = groupByHour(tbl_c);
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
            var calendar = calIdToCalendar[m.calId];
            if (dayInCalendar (date, calendar) &&
                timeAfter (h + ":" + m.min, date)) {
                minute.style.textDecoration = "underline";
            }
            minute.appendChild(document.createTextNode(m.min));
            if ((calendar.added_excn && calendar.added_excn.length > 0) ||
                (calendar.remov_excn && calendar.remov_excn.length > 0)) {
                var calSub = document.createElement('sub');
                calSub.appendChild(document.createTextNode(m.calId));
                minute.appendChild(calSub);
            }
            node.appendChild(minute);
        }
        table.appendChild(node);
    }
    disp.appendChild(table);
}

function createCalLegend(calIdToCalendar) {
    var legend = document.createElement('table');
    legend.style.borderCollapse = "collapse";
    var row = document.createElement('tr');
    var col = document.createElement('th');
    col.style.border = "1px solid";
    col.appendChild(document.createTextNode(msg11));
    row.appendChild(col);
    col = document.createElement('th');
    col.style.border = "1px solid";
    col.appendChild(document.createTextNode(msg10));
    row.appendChild(col);
    col = document.createElement('th');
    col.style.border = "1px solid";
    col.appendChild(document.createTextNode(msg9));
    row.appendChild(col);
    legend.appendChild(row);
    var hasExceptions = false;
    for (var id in calIdToCalendar) {
        var calendar = calIdToCalendar[id];
        if (!(calendar.added_excn && calendar.added_excn.length > 0) &&
            !(calendar.remov_excn && calendar.remov_excn.length > 0)) {
            continue;
        }
        hasExceptions = true;
        row = document.createElement('tr');
        col = document.createElement('td');
        col.style.border = "1px solid";
        col.appendChild(document.createTextNode(id));
        row.appendChild(col);
        col = document.createElement('td');
        col.style.border = "1px solid";
        if (calendar.remov_excn && calendar.remov_excn.length > 0) {
            col.appendChild(document.createTextNode(printDateList(
                calendar.remov_excn)));
        } else {
            col.appendChild(document.createTextNode(msg12));
        }
        row.appendChild(col);
        col = document.createElement('td');
        col.style.border = "1px solid";
        if (calendar.added_excn && calendar.added_excn.length > 0) {
            col.appendChild(document.createTextNode(printDateList(
                calendar.added_excn)));
        } else {
            col.appendChild(document.createTextNode(msg12));
        }
        row.appendChild(col);
        legend.appendChild(row);
    }
    return hasExceptions ? legend : null;
}

function printDateList(dates) {
    return dates.map(expandDate).join(' ');
}

function expandDate(date) {
    return /^\d\d\d\d\d\d\d\d$/.test(date) ?
        date.substring(0, 4) + '.' + date.substring(4, 6) + '.' +
        date.substring(6, 8) :
        date;
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

// With Ids, the preprocessing here is not really needed.
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
    console.log('DEBUG: tbl=', tbl);
    var grouped = new Map();
    for (var i = 0; i < tbl.length; i++) {
        var v = tbl[i].time.split(':');
        var k = v[0];
        if (k.length == 1) k = "0" + k;
        var min = v.length > 1 ? v[1] : '0';
        console.log('DEBUG: time=', tbl[i].time, ' k=', k, ' min=', min);
        if (!(k in grouped)) grouped[k] = new Array();
        grouped[k].push({min: min, calId: tbl[i].calId});
    }
    return grouped;
}

window.addEventListener('load', initialize);
