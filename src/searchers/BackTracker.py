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
            # print ( "--------------" )
            # print ( "day: {}".format(day) )
            # print ( "cur_city: {}".format(cur_city) )
            if day not in possible_flights.keys():
                possible_flights[day] = dataset.get_flights(cur_city,
                                                            day,
                                                            cities_to_visit=cities_to_visit,
                                                            sort_by_price=True)
            # print ( "possible_flights[day]: {}".format(possible_flights[day]) )
            if not possible_flights[day]:
                assert day != 0, "day 0 and nowhere to go  \
                                  - either a bug or no cycle in data"
                #backwards
                # print ( "---- backing from: " )
                # print ( "day: {}".format(day) )
                # print ( "trip: {}".format(trip) )
                # print ( "cities to visit: {}".format(cities_to_visit) )
                # print ( "Nowhere to go: returning " )
                # print ( "possible_flights[day]: {}".format(possible_flights[day]) )
                del possible_flights[day]

                last_flight = trip.pop(-1)
                cities_to_visit.append(cur_city)
                day -= 1
                assert day >= 0, "bug: returning before day 0"

            else:
                #forward
                flight_taken = possible_flights[day].pop(0)
                trip.append(flight_taken)
                cities_to_visit.remove(flight_taken.city_to)
                cur_city = flight_taken.city_to
                day += 1

            # return to starting city:
            if not cities_to_visit:
                possibilities = dataset.get_flights(cur_city,
                                                    day,
                                                    cities_to_visit=[start_city],
                                                    sort_by_price=True)
                if possibilities:
                    trip.append(possibilities[0])
                else:
                    last_flight = trip.pop(-1)
                    cities_to_visit.append(cur_city)
                    day -= 1
                    assert day >= 0, "bug: returning before day 0"

        return trip
