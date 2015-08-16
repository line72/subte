Subte jest aplikacją do zarządzania danymi transportu publicznego. Pozwala nanosić przystanki, trasy i rozkłady jazdy, i eksportować dane do GTFS (General Transit Feed Specification), które może być użyte przez Google Transit, Open Trip Planner, i inne systemy.

Program zaimplementował Marcus Dillavou <line72@line72.net> (http://line72.net) by pomóc w budowaniu rozkładów jazdy dla BJCTA [Birmingham-Jefferson County Transit Authority] (http://www.bjcta.org) w Birmingham, AL. Po więcej informacji o tym projekcie, zajrzyj na:

http://line72.net/index.php/software/subte/

Program został rozwinięty przez Łukasza Stafiniaka <lukstafi@gmail.com> o:
* drobne zmiany które zdają się poprawiać niezawodność interfejsu (program nie działał u Łukasza bez nich),
* pola dialogowe do edycji danych przewoźników,
* eksport plików KML i JSON /Javascript z danymi, i pliki `utils/display_map.html`, `utils/display_map.js`, które razem tworzą minimalistyczną aplikację webową opartą o Google Maps do odczytywania rozkładów jazdy,
* przetłumaczenie interfejsu na język polski, lokalizacja jest ustalana przez ustawienia systemowe.

To oprogramowanie jest na licencji GPLv3 lub późniejszej.

## Obsługa

Przytrzymaj wskaźnik myszy nad elementem interfejsu żeby zobaczyć pomoc w dymku. Żeby wprowadzić nowe godziny w tabeli ''Kursy'': kliknij na przycisk ''Dodaj'', kliknij dwa-trzy razy na komórce odpowiadającej przystankowi, aż pojawi się pole edycyjne, wpisz godzinę odjazdu z przystanku w formacie GG:MM lub GG:MM:SS, wciśnij `enter`. Czasy powinny zawsze wzrastać wzdłuż trasy, użyj `24:05` na odjazd 5 minut kolejnego dnia, `25:00` na pierwszą w nocy kolejnego dnia, itd. Przed kliknięciem na przystanek na mapie, możesz potrzebować kliknąć na dymek poprzednio klikniętego przystanku, żeby znikł.

Pamiętaj żeby wypełnić wszystkie pola z rozwijanymi opcjami przed dodaniem nowego zestawu kursów, nowego przystanku itd. Jeśli rozwijana lista dla danego pola jest pusta, musisz dodać nową opcję przez kliknięcie guzika `Dodaj` na prawo od danego pola. Patrz uwagi o polach wymaganych poniżej.

Terminologia:
* ''Kalendarz'' podaje dni kursów autobusowych, tzn. w które dni dokładnie jedzie autobus.
* ''Trasa'' (pomimo nazwy) podaje przewoźnika i kalendarz (tzn. dni kursowania) kursów autobusowych.
* ''Grupa kursów'' podaje przystanki i godziny kursów autobusowych (i informacje powyżej, przez wybór trasy i kalendarza).

Niestety, jeśli kurs kursuje o pewnej godzinie z wyjątkiem specyficznych dni, albo dodatkowo w specyficzne dni, musisz stworzyć nowy kalendarz i nową grupę kursów specjalnie dla tej godziny i dla innych godzin mających ten sam wyjątek, tzn. kursujących w dokładnie te same dni.

Zamierzone znaczenie pól w programie pochodzi ze specyfikacji GTFS:
[General Transit Feed Specification Reference](https://developers.google.com/transit/gtfs/reference).
Jednak, na potrzeby minimalistycznego interfejsu webowego wspomnianego poniżej, tylko następujące pola są wymagane:
* Albo nazwa (preferowane), albo opis przystanku.
* Położenie przystanku (które możesz wprowadzić klikając na mapie podczas gdy okno `Dodaj przystanek` jest otwarte).
* Trasa grupy kursów (kliknij przycisk `Dodaj` na prawo od menu rozwijalnego jeśli dana grupa kursów potrzebuje nowej trasy).
* Kalendarz grupy kursów (kliknij przycisk `Dodaj` na prawo od menu rozwijalnego jeśli dana grupa kursów potrzebuje nowego kalendarza).
* Wszystkie pola w kalendarzu z wyjątkiem daty początku i końca obowiązywania:
** nazwa kalendarza,
** dni kursowania,
** dodatkowe dni "też kursuje", jeśli są takie,
** wykluczone dni "nie kursuje", jeśli są takie.
* Czasy odjazdów, po kliknięciu guzika na prawo od `Edytuj kursy:` (frekwencje kursów, jak w przycisku poniżej, nie są obsługiwane przez minimalistyczny interfejs webowy);
** uwaga: najpierw dodaj przystanki grupy kursów, dodatkowo możesz potrzebować powiększyć okno `Edytuj kursy`.
* Albo skrócona nazwa, albo pełna nazwa trasy.
* Przewoźnik trasy (kliknij przycisk `Dodaj` na prawo od menu rozwijalnego jeśli trasa potrzebuje nowego przewoźnika).
* Nazwa przewoźnika.

Poniższe pola są obecnie ignorowane przez minimalistyczny interfejs webowy:
* nazwa grupy kursów,
* tablica na autobusie dla grupy kursów,
* frekwencje grupy kursów,
* data początku i końca obowiązywania kalendarza,
* informacje o przewoźnikach inne niż ich nazwa.

By dostarczyć minimalistycznego webowego interfejsu do rozkładów jazdy:
* wyeksportuj dane klikając na przycisk `Eksportuj do KML z tablicami` lub przycisk `Eksportuj do KML z linkami` i wybierając pusty katalog,
* przenieś wszystkie pliki wygenerowane w powyższym katalogu do docelowego katalogu z web-hostingiem,
* skopiuj pliki `utils/display_map.html`, `utils/display_map.js` i `utils/display_stop.js` do docelowego katalogu z web-hostingiem,
* interfejs będzie dostępny pod adresem webowym pliku `display_map.html`.

(Plik `doc.kml` jest cache'owany przez przeglądarkę, więc możesz potrzebować zmieniać jego nazwę, również w pliku `display_map.js`, ewentualnie czyścić cache przeglądarki, by testować rezultaty podczas rozwijania aplikacji.)

By dostarczyć dane serwisowi Google Transit, kliknij na przycisk `Eksportuj do GTFS`, spakuj wygenerowane pliki z rozszerzeniem `.txt` jako archiwum `.zip`, i wykonaj polecenia z [Google Transit Partner Program](https://maps.google.com/help/maps/mapcontent/transit/participate.html). Ale to wymaga autoryzacji od firm przewoźniczych.

Dane mogą być też użyte z aplikacjami [Open Trip Planner](http://www.opentripplanner.org/), na przykład [OpenTripPlanner for Android](https://github.com/CUTR-at-USF/OpenTripPlanner-for-Android/wiki). Ale to wymaga postawienia serwera Open Trip Planner.

## Instalowanie pod Linuxem

Pobierz i rozpakuj źródła: np. kliknij na guzik `Download ZIP` na [https://github.com/lukstafi/subte](https://github.com/lukstafi/subte) i rozpakuj archiwum. Wejdź do katalogu, np.:

```
$ cd subte-master
```

Pod Fedora Linux, zainstaluj:

```
$ yum install gobject-introspection libchamplain-gtk python-exif \
 python-pillo python-lxml python-dateutil clutter-gtk
```

Pod Ubuntu Linux, zainstaluj:

```
$ sudo apt-get install gobject-introspection libchamplain-gtk-0.12-0 \
 python-exif python-pil python-lxml python-dateutil \
 libclutter-gtk-1.0-0 gir1.2-gtkclutter-1.0 gir1.2-champlain-0.12 \
 gir1.2-gtk-3.0 gir1.2-gtkchamplain-0.12
```

Potem możesz uruchomić bezpośrednio:

```
$ ./subte
```

lub możesz zainstalować

```
$ python setup.py build
$ python setup.py install
$ subte
```

Poniższe informacje tylko po angielsku.

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
