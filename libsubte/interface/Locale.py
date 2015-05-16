# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 - Lukasz Stafiniak
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

import locale

loc_language = locale.getlocale()

dict_pl = {
    'Path: ': u'Ścieżka: ',
    'Path': u'Ścieżka',
    'Add Route': u'Dodaj trasę',
    'Add': u'Dodaj',
    'Cancel': u'Anuluj',
    'Edit Route': u'Edytuj trasę',
    'Edit': u'Edytuj',
    'Short Name: ': u'Skrócona nazwa: ',
    'Long Name: ': u'Pełna nazwa: ',
    'Description: ': u'Opis: ',
    'Route: ': u'Trasa: ',
    'Add Agency': u'Dodaj przewoźnika',
    'Edit Agency': u'Edytuj przewoźnika',
    'Name: ': u'Nazwa: ',
    'URL: ': u'Adres www: ',
    'Timezone: ': u'Strefa czasowa: ',
    'Language: ': u'Język: ',
    'Phone: ': u'Telefon: ',
    'Fare URL: ': u'Adres www zakupu biletów: ',
    'Agency: ': u'Przewoźnik: ',
    'Picture': u'Obrazek',
    'Trip Route': u'Kursy trasy',
    'Stop': u'Przystanek',
    'Merge Stops': u'Połącz przystanki',
    'Merge': u'Połącz',
    'Stop 1: ': u'Przystanek 1',
    'Stop 2: ': u'Przystanek 2',
    'Edit Trips': u'Edytuj kursy',
    'Edit Trips: ': u'Edytuj kursy: ',
    'Close': u'Zamknij',
    'Outbound': u'Wyjazdowy',
    'Inbound': u'Przyjazdowy',
    'Add Calendar': u'Dodaj daty',
    'Edit Calendar': u'Edytuj daty',
    'Monday': u'Poniedziałek',
    'Tuesday': u'Wtorek',
    'Wednesday': u'Środa',
    'Thursday': u'Czwartek',
    'Friday': u'Piątek',
    'Saturday': u'Sobota',
    'Sunday': u'Niedziela',
    'Start date: ': u'Począwszy od: ',
    'End date: ': u'Obowiązuje do: ',
    'Added days: ': u'Też kursuje: ',
    'Removed days: ': u'Nie kursuje: ',
    'Calendar: ': u'Daty: ',
    'Add Stop': u'Dodaj przystanek',
    'Edit Stop': u'Edytuj przystanek',
    'Latitude: ': u'Szerokość geo.: ',
    'Longitude: ': u'Wysokość geo.: ',
    'Import from...': u'Importuj z...',
    'Export to...': u'Eksportuj do...',
    'Stops': u'Przystanki',
    'Trips': u'Kursy',
    'Paths': u'Ścieżki',
    'Load a project': u'Wczytaj projekt',
    'Save a project': u'Zapisz projekt',
    'Close a project': u'Zamknij projekt',
    'Add a new stop': u'Dodaj nowy przystanek',
    'Edit a new stop': u'Edytuj przystanek',
    'Remove a stop': u'Usuń przystanek',
    'Merge two stops': u'Połącz dwa przystanki',
    'Add a new trip': u'Dodaj nową grupę kursów',
    'Edit a trip': u'Edytuj grupę kursów',
    'Remove a trip': u'Usuń grupę kursów',
    'Copy a trip': u'Kopiuj grupę kursów',
    'Add a new picture': u'Dodaj nowy obrazek',
    'Add a new path from a .kml (or .kmz) file': u'Dodaj nową ścieżkę z pliku .kml (lub .kmz)',
    'Remove a path': u'Usuń ścieżkę',
    'Import': u'Importuj',
    'Import GTFS': u'Importuj GTFS',
    'Export': u'Eksportuj',
    'Export to Google': u'Eksportuj do Google',
    'Stops: ': u'Przystanki: ',
    'Trips: ': u'Kursy: ',
    'Modify Trips': u'Modyfikuj kursy',
    'Add Trip': u'Dodaj grupę kursów',
    'Edit Trip': u'Edytuj grupę kursów',
    'Next Trip': u'Kolejny kurs autobusu',
    'Headsign: ': u'Tablica na autobusie: ',
    'Direction: ': u'Kierunek: ',
    'Edit Frequencies: ': u'Edit Frequencies: ',
    ' Copy': u' kopia',
    'What riders use to identify a route, e.g. a number': u'Jak pasażerowie nazywają trasę, np. numer',
    'More descriptive name, e.g. including destination': u'Bardziej opisowa nazwa, np. zawierająca cel',
    'Useful information on how the route operates': u'Użyteczna informacja o działaniu trasy',
    'Click a stop on the map to add': u'Kliknij przystanek na mapie żeby dodać',
    'Stop name understandable to riders': u'Nazwa przystanku zrozumiała dla pasażerów',
    'Additional information about the stop': u'Dodatkowe informacje o przystanku',
    'Full name of the agency': u'Pełna nazwa przewoźnika',
    'Must begin with http:// or https://': u'Musi zaczynać się od http:// lub https://',
    'A calendar specifies dates on which a group of trips run': u'Daty wyznaczają dni w których dana grupa kursów jeździ',
    'Date format: eight digits YYYYMMDD': u'Format daty: osiem cyfr RRRRMMDD (rok miesiąc dzień)',
    'Days in YYYYMMDD format separated by spaces': u'Dni w formacie RRRRMMDD rozdzielone spacjami',
    'Paths (optional) provide Google Maps the exact curve that a bus follows': u'Ścieżki (opcjonalne) dostarczają Google Maps dokładnej krzywej po której porusza się autobus',
    'A group of trips sharing a route and days of operation': u'Grupa kursów na tej samej trasie operujących w tych samych dniach',
    'A sign on the bus identifying the destination': u'Tablica lub napis na autobusie identyfikująca cel podróży',
    'Distinguish trips on routes that go both ways': u'Rozróżnij kursy na trasach z kursami w dwie strony',
    'Enter times at which trips leave stops': u'Wprowadź godziny odjazdów kursów z przystanków',
    'Click on the map to enter coordinates': u'Kliknij na mapie żeby wprowadzić współrzędne'    
}

def _(s):
    if loc_language[0].upper()[0:2] == 'PL':
        return dict_pl[s]
    else:
        return s