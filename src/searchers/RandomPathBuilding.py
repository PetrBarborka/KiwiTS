from copy import deepcopy
from random import randint


class RandomPathBuilding:
    def __init__(self):
        pass

    def search(self, dataset):
        starting_city = dataset.get_starting_city()
        cities_to_visit = deepcopy(dataset.cities)
        cities_to_visit.remove(starting_city)

        current_city = starting_city
        current_day = 0

        trip = []

        while cities_to_visit:
            possible_flights = dataset.get_flights(current_city, current_day, cities_to_visit=cities_to_visit,
                                                   sort_by_price=True)

            if not possible_flights:
                return None
            else:
                upper_range = int(len(possible_flights) / 10)
                if upper_range == 0:
                    upper_range = len(possible_flights) - 1
                flight_to_take = randint(0, upper_range)
                flight_taken = possible_flights[flight_to_take]

                trip.append(flight_taken)
                cities_to_visit.remove(flight_taken.city_to)

                current_city = flight_taken.city_to
                current_day += 1

            if not cities_to_visit:
                possible_flights = dataset.get_flights(current_city, current_day, cities_to_visit=[starting_city],
                                                       sort_by_price=True)

                if not possible_flights:
                    return None
                else:
                    trip.append(possible_flights[0])
                    return trip
