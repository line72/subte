import os

import gtbuilder

def build_stops():
    stops = gtbuilder.Stop.load_stops(os.path.join('timetables', 'stops.csv'))

    # stops.append(gtbuilder.Stop(stop_id = 'central', name = 'Central Station',
    #                             latitude = 33.511878, longitude = -86.808826,
    #                             zone_id = 'zone1'))
    # stops.append(gtbuilder.Stop(stop_id = 'MorrisA20S', name = 'Morris Ave & 20th Street',
    #                             latitude = 33.51382, longitude = -86.80521,
    #                             zone_id = 'zone1'))
    # stops.append(gtbuilder.Stop(stop_id = '5points', name = '5 Points South',
    #                             latitude = 33.50062, longitude = -86.79630,
    #                             zone_id = 'zone1'))
    # stops.append(gtbuilder.Stop(stop_id = 'summit', name = 'Summit', description = 'Summit Shopping Center',
    #                             latitude = 33.44800, longitude = -86.73103,
    #                             zone_id = 'zone1'))
    # stops.append(gtbuilder.Stop(stop_id = 'colonnade', name = 'Colonnade',
    #                             latitude = 33.43941, longitude = -86.72557,
    #                             zone_id = 'zone1'))
    # stops.append(gtbuilder.Stop(stop_id = 'marriott280', name = 'Marriott Grandview',
    #                             latitude = 33.43841, longitude = -86.72389,
    #                             zone_id = 'zone1'))
    # stops.append(gtbuilder.Stop(stop_id = 'chickfila280', name = 'Chick-fil-a',
    #                             latitude = 33.428422, longitude = -86.707752,
    #                             zone_id = 'zone1'))
    # stops.append(gtbuilder.Stop(stop_id = 'walmart280', name = 'Super Walmart 280',
    #                             latitude = 33.42145, longitude = -86.67592,
    #                             zone_id = 'zone1'))
    return stops

def build_routes():
    routes = []

    routes.append(build_hwy280())

def build_hwy280():
    # create a route
    hwy280 = gtbuilder.Route('hwy280', agency, 'HWY280',
                   description = 'This route goes from Central Station down US280 to the Super Walmart',
                   route_type = 3)

    # our calendars
    weekdays = gtbuilder.Calendar.get_calendar('WD')
    saturday = gtbuilder.Calendar.get_calendar('S')

    # start building our trips
    hwy280.build_trips(os.path.join('timetables', 'hwy280WD.csv'), weekdays, 'hwy280WD')
    hwy280.build_trips(os.path.join('timetables', 'hwy280S.csv'), saturday, 'hwy280S')

    return hwy280

if __name__ == '__main__':
    # build our agency
    agency = gtbuilder.Agency(agency_id = 'bjcta',
                              name = 'Birmingham-Jefferson County Transit Authority',
                              url = 'http://www.bjcta.org', phone = '205-521-0161',
                              fare_url = 'http://www.bjcta.org/fares/fare_structure.cfm')

    # build some stops
    stops = build_stops()

    # create some calendars
    weekdays = gtbuilder.Calendar('WD', 1, 1, 1, 1, 1, start_date = '20110101', end_date = '20130101')
    saturday = gtbuilder.Calendar('S', saturday = 1, start_date = '20110101', end_date = '20130101')

    # start building our routes and trips
    routes = build_routes()

    # write everything
    gtbuilder.write()
