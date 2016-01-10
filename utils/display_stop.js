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
    var date = new Date();
    var tomorrow = new Date();
    tomorrow.setDate(date.getDate() + 1);
    var spans = document.getElementsByTagName('span');
    for (i = 0; i < spans.length; i++) {
        if (spans[i].hasAttribute("cal-name") &&
            dayInCalendar
              (date, calendars[spans[i].getAttribute("cal-name")]) &&
               timeAfter (spans[i].getAttribute("trip-time"), date)) {
            // spans[i].style.color = "red";
            spans[i].style.textDecoration = "underline";
        }
        if (spans[i].hasAttribute("cal-label") &&
            dayInCalendar
              (tomorrow, calendars[spans[i].getAttribute("cal-label")])) {
            // spans[i].style.color = "red";
            spans[i].style.textDecoration = "underline";
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

window.addEventListener('load', initialize);
