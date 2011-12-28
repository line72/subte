
import gtbuilder

if __name__ == '__main__':
    agency = gtbuilder.Agency(agency_id = 'bjcta',
                              name = 'Birmingham-Jefferson County Transit Authority',
                              url = 'http://www.bjcta.org', phone = '205-521-0161',
                              fare_url = 'http://www.bjcta.org/fares/fare_structure.cfm')

    # build some stops
    stops = []
    stops.append(gtbuilder.Stop(stop_id = 'central', name = 'Central Station',
                      latitude = 33.511878, longitude = -86.808826,
                      zone_id = 'zone1'))
    stops.append(gtbuilder.Stop(stop_id = 'summit', name = 'Summit', description = 'Summit Shopping Center',
                      latitude = 33.44800, longitude = -86.73103,
                      zone_id = 'zone1'))
    stops.append(gtbuilder.Stop(stop_id = 'marriott280', name = 'Marriott Grandview',
                      latitude = 33.43841, longitude = -86.72389,
                      zone_id = 'zone1'))
    stops.append(gtbuilder.Stop(stop_id = 'chickfila280', name = 'Chick-fil-a',
                      latitude = 33.428422, longitude = -86.707752,
                      zone_id = 'zone1'))
    stops.append(gtbuilder.Stop(stop_id = 'walmart280', name = 'Super Walmart 280',
                      latitude = 33.42145, longitude = -86.67592,
                      zone_id = 'zone1'))

    # create some calendars
    weekdays = gtbuilder.Calendar('WD', 1, 1, 1, 1, 1, start_date = '20110101', end_date = '20130101')
    saturday = gtbuilder.Calendar('S', saturday = 1, start_date = '20110101', end_date = '20130101')

    # create a route
    hwy280 = gtbuilder.Route('hwy280', agency, 'HWY280',
                   description = 'This route goes from Central Station down US280 to the Super Walmart',
                   route_type = 3)
    hwy280_wd1 = hwy280.add_trip('hwy280WD1', weekdays)
    hwy280_wd1.add_stop(gtbuilder.Stop.get_stop('central'), '04:50:00')
    hwy280_wd1.add_stop(gtbuilder.Stop.get_stop('summit'), '05:15:00')
    hwy280_wd1.add_stop(gtbuilder.Stop.get_stop('marriott280'), '05:37:00')

    # write everything
    gtbuilder.write()
    #gtbuilder.Agency.write_agencies()
    #gtbuilder.Stop.write_stops()
    #gtbuilder.Route.write_routes()
