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

By dostarczyć minimalistycznego webowego interfejsu do rozkładów jazdy:
* wyeksportuj dane klikając na przycisk `Eksportuj do Google`,
* przenieś pliki `doc.kml` i `doc.js` do docelowego katalogu z web-hostingiem,
* edytuj pliki `utils/display_map.html`, `utils/display_map.js`: zamień wszystkie wystąpienia `https://ENTER YOUR URL HERE/` przez adres webowy,
* skopiuj pliki `utils/display_map.html`, `utils/display_map.js` do docelowego katalogu z web-hostingiem,
* interfejs będzie dostępny pod adresem webowym pliku `display_map.html`.

(Plik `doc.kml` jest cache'owany przez przeglądarkę, więc możesz potrzebować zmieniać jego nazwę, również w pliku `display_map.js`, ewentualnie czyścić cache przeglądarki, by testować rezultaty podczas rozwijania aplikacji.)

By dostarczyć dane serwisowi Google Transit, spakuj pliki z rozszerzeniem `.txt` jako archiwum `.zip`, i wykonaj polecenia z [Google Transit Partner Program](https://maps.google.com/help/maps/mapcontent/transit/participate.html). Ale to wymaga autoryzacji od firm przewoźniczych.

Dane mogą być też użyte z aplikacjami [Open Trip Planner](http://www.opentripplanner.org/), na przykład [OpenTripPlanner for Android](https://github.com/CUTR-at-USF/OpenTripPlanner-for-Android/wiki). Ale to wymaga postawienia serwera Open Trip Planner.

Instrukcje instalowania programu ze źródeł są w języku angielskim poniżej.

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

$ sudo apt-get install gobject-introspection libchamplain-gtk-0.12-0 python-exif python-pil python-lxml python-dateutil libclutter-gtk-1.0-0 gir1.2-gtkclutter-1.0 gir1.2-champlain-0.12 gir1.2-gtk-3.0 gir1.2-gtkchamplain-0.12

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