import os
import sys
import gtbuilder

def main(input_directory):
    db = gtbuilder.Database()

    # agency
    agency_ids = {}
    try:
        f = open(os.path.join(input_directory, 'agency.txt'), 'r')
        header = f.readline()

        for l in f.readlines():
            t = l.split(',')
            if len(t) != 6:
                print >> sys.stderr, 'Invalid agency', t
                continue

            agency = gtbuilder.Agency(name = t[1], url = t[2],
                                      timezone = t[3], language = t[5], phone = t[4])
            agency_ids[t[0]] = agency

        f.close()
    except IOError, e:
        print >> sys.stderr, 'Warning, no agency file'

    # calendar
    calendar_ids = {}
    try:
        f = open(os.path.join(input_directory, 'calendar.txt'), 'r')
        header = f.readline()

        for l in f.readlines():
            t = l.split(',')
            if len(t) != 10:
                print >> sys.stderr, 'Invalid calendar', t
                continue

            calendar = gtbuilder.Calendar(t[0], int(t[1]), int(t[2]), int(t[3]),
                                          int(t[4]), int(t[5]), int(t[6]), int(t[7]),
                                          t[8], t[9])
            calendar_ids[t[0]] = calendar
        f.close()
    except IOError, e:
        print >> sys.stderr, 'Warning, no calendar file'

    # calendar exceptions
    #!mwd - we don't support this yet

    # stops
        
    # this dictionary holds a key/value pair relating
    #  the original id with our internal id
    stop_ids = {} 
    try:
        f = open(os.path.join(input_directory, 'stops.txt'), 'r')
        header = f.readline()

        for l in f.readlines():
            t = l.split(',')
            if len(t) != 8:
                print >> sys.stderr, 'Invalid stop', t
                continue

            lat = float(t[3])
            lon = float(t[4])

            # see if we have a stop at this location
            stop = None
            for i in reversed(gtbuilder.Stop.stops):
                if i.latitude == lat and i.longitude == lon:
                    print >> sys.stderr, 'Found existing stop', [i.name, i.description, i.latitude, i.longitude], t
                    stop = i
                    break
                
            if stop is None: # no match
                stop = gtbuilder.Stop(name = t[1], description = t[2],
                                      latitude = lat, longitude = lon)
            # link with original id
            stop_ids[t[0]] = stop
                                  

        f.close()
    except IOError, e:
        print >> sys.stderr, 'Warning, no stops file'


    # routes
    route_ids = {}
    try:
        f = open(os.path.join(input_directory, 'routes.txt'), 'r')
        header = f.readline()

        for l in f.readlines():
            t = l.split(',')
            if len(t) != 6:
                print >> sys.stderr, 'Invalid route', t
                continue

            agency = agency_ids.get(t[1], None)
            if agency is None:
                print >> sys.stderr, 'Warning, invalid agency', t[1]
                continue

            route = gtbuilder.Route(agency, t[2], t[3], t[4], int(t[5]))
            route_ids[t[0]] = route

        f.close()
    except IOError, e:
        print >> sys.stderr, 'Warning, no routes file'

    # # trips
    # trip_ids = {}
    # try:
    #     f = open(os.path.join(input_directory, 'trips.txt'), 'r')
    #     header = f.readline()

    #     for l in f.readlines():
    #         t = l.split(',')
    #         if len(t) != 5:
    #             print >> sys.stderr, 'Invalid trip', t
    #             continue

    #         route = route_ids.get(t[0], None)
    #         if route is None:
    #             print >> sys.stderr, 'Warning, invalid route_id', t[0]
    #             continue
    #         calendar = calendar_ids.get(t[1], None)
    #         if calendar is None:
    #             print >> sys.stderr, 'Warning, invalid calendar_id', t[1]
    #             continue

    #         trip = route.add_trip(t[2], calendar)
    #         trip_ids[t[2]] = trip

    #     f.close()
    # except IOError, e:
    #     print >> sys.stderr, 'Warning, no trips file'

    # # stop times

    # # we parse stop times first, one is to find all the stops 
    # #  associated with a route, then to go back and add them
    # #  to each trip.
    # # This is difficult since our routes can't hold duplicate stop
    # stop_time_ids = {}
    # try:
    #     f = open(os.path.join(input_directory, 'stop_times.txt'), 'r')
    #     header = f.readline()

    #     for l in f.readlines():
    #         t = l.split(',')
    #         if len(t) != 9:
    #             print >> sys.stderr, 'Invalid stop_time', t
    #             continue

    #         trip = trip_ids.get(t[0], None)
    #         if trip is None:
    #             print >> sys.stderr, 'Warning, invalid trip_id', t[0]
    #             continue
    #         stop = stop_ids.get(t[3], None)
    #         if stop is None:
    #             print >> sys.stderr, 'Warning, invalid stop_id', t[3]
    #             continue
            
    #         if stop not in trip.route.stops:
    #             trip.route.add_stop(stop)

    #         if t[0] not in stop_time_ids:
    #             stop_time_ids[t[0]] = {}
    #         # match the stop_sequence with the stop
    #         stop_time_ids[t[0]][t[4]] = stop

    #         print 'adding stop to trip', trip, stop, t[1], t[2]
    #         trip.update_stop(stop, t[1], t[2])

    #     f.close()

    # except IOError, e:
    #     print >> sys.stderr, 'Warning, no stop_times file'



    # write out
    db.save(input_directory)
    # export
    exported = os.path.join(input_directory, 'exported')
    try: os.makedirs(exported)
    except OSError, e: pass
    db.export(exported)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print >> sys.stderr, 'Usage: %s input_directory' % sys.args[0]
        sys.exit(1)

    main(sys.argv[1])
