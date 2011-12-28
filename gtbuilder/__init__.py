from Agency import Agency
from Route import Route
from Stop import Stop
from Calendar import Calendar
from Trip import Trip

def write():
    Agency.write_agencies()
    Stop.write_stops()
    Route.write_routes()
    Calendar.write_calendars()
    Trip.write_trips()
