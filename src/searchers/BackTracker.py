from copy import deepcopy

class BackTracker:
    def __init__(self):
        pass

    def search(self, dataset):

        trip = []
        #possible_flights = { day : [flight flight flight ... ] }
        # je to vpodstate stack
        possible_flights = {}

        start_city = dataset.get_starting_city()
        cities_to_visit = deepcopy(dataset.cities)
        cities_to_visit.remove(start_city)

        day = 0
        cur_city = start_city

        while(cities_to_visit):
            possible_flights[day] = dataset.get_flights(cur_city,
                                                        day,
                                                        cities_to_visit=cities_to_visit,
                                                        sort_by_price=True)
            if not possible_flights[day]:
                print ( "day: {}".format(day) )
                print ( "trip: {}".format(trip) )
                print ( "cities to visit: {}".format(cities_to_visit) )
                print ( "Nowhere to go !!!!" )
                return None
            flight_taken = possible_flights[day].pop(0)
            trip.append(flight_taken)
            cities_to_visit.remove(flight_taken.city_to)
            cur_city = flight_taken.city_to
            day += 1

            if not cities_to_visit and not flight_taken.city_to == start_city:
                cities_to_visit = [start_city]

        return trip
