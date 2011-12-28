import os

import gtbuilder

def build_stops():
    stops = gtbuilder.Stop.load_stops(os.path.join('timetables', 'stops.csv'))

    return stops

def build_routes():
    routes = []

    routes.append(build_r1())
    routes.append(build_r3())
    routes.append(build_hwy280())
    

def build_r1():
    '''South Bessemer'''
    r1 = gtbuilder.Route('route1', agency, '1',
                         description = 'South Bessemer - This route goes down US 11 to Bessemer',
                         route_type = 3)

    # our calendars
    weekdays = gtbuilder.Calendar.get_calendar('WD')
    saturday = gtbuilder.Calendar.get_calendar('S')

    # start building our trips
    r1.build_trips(os.path.join('timetables', 'R1WD.csv'), weekdays, 'R1WD')
    r1.build_trips(os.path.join('timetables', 'R1S.csv'), saturday, 'R1S')

    return r1

def build_r3():
    '''Jefferson/Wenonah'''
    r3 = gtbuilder.Route('route3', agency, '3',
                         description = 'Jefferson/Wenonah',
                         route_type = 3)

    # our calendars
    weekdays = gtbuilder.Calendar.get_calendar('WD')
    saturday = gtbuilder.Calendar.get_calendar('S')

    # start building our trips
    r3.build_trips(os.path.join('timetables', 'R3WD.csv'), weekdays, 'R3WD')
    r3.build_trips(os.path.join('timetables', 'R3S.csv'), saturday, 'R3S')

    return r3


def build_hwy280():
    # create a route
    hwy280 = gtbuilder.Route('hwy280', agency, 'HWY280',
                   description = 'HWY280 Limited - This route goes from Central Station down US280 to the Super Walmart',
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
