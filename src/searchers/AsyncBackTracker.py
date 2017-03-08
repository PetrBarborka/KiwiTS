from copy import deepcopy
import sys, os
sys.path.append(os.path.realpath(".."))

from datasets import DataPath


class AsyncBackTracker:

    def __init__(self, dataset, register_result_callback):
        self.dataset = dataset
        self.register_result = register_result_callback

    def search(self):

        trip = []
        #possible_flights = { day : [flight flight flight ... ] }
        # je to vpodstate stack
        possible_flights = {}

        start_city = self.dataset.get_starting_city()
        cities_to_visit = deepcopy(self.dataset.cities)
        cities_to_visit.remove(start_city)

        day = 0
        cur_city = start_city

        while(cities_to_visit):
            if day not in possible_flights.keys():
                possible_flights[day] = self.dataset.get_flights(cur_city,
                                                            day,
                                                            cities_to_visit=cities_to_visit,
                                                            sort_by_price=True)
            if possible_flights[day]:
                #forward
                # print( "forward" )

                flight_taken = possible_flights[day].pop(0)
                trip.append(flight_taken)
                cities_to_visit.remove(flight_taken.city_to)
                cur_city = flight_taken.city_to
                day += 1

            else:
                #backwards
                # print( "backwards" )
                
                if day == 0:
                    # print ( "self.dataset exhausted" )
                    return

                assert day != 0, "day 0 and nowhere to go  \
                                  - either a bug or no cycle in data"
                del possible_flights[day]

                last_flight = trip.pop(-1)
                cities_to_visit.append(cur_city)
                cur_city = last_flight.city_from
                day -= 1
                assert day >= 0, "bug: returning before day 0"

            # return to starting city:
            if not cities_to_visit:
                # print( "returning" )
                return_possibilities = self.dataset.get_flights( cur_city,
                                                            day,
                                                            cities_to_visit=[start_city],
                                                            sort_by_price=True )
                while( return_possibilities ):

                    flight_taken = return_possibilities.pop(0)
                    trip.append( flight_taken )
                    price = sum([f.price for f in trip])
                    path = DataPath(trip, price)

                    self.register_result( path )

                    trip.pop(-1)

                last_flight = trip.pop(-1)
                cities_to_visit.append(cur_city)
                cur_city = last_flight.city_from
                day -= 1
                assert day >= 0, "bug: returning before day 0"

if __name__ == "__main__":

    def register_result(path):
        validity = "VALID" if path.is_valid() else "NON-VALID"
        print( "found {} path for: {}".format( validity, path.price ) )

    import sys, os
    sys.path.append(os.path.realpath(".."))
    from datasets.CDictDataset import CDictDataset

    input_file = "../../benchmark/benchmarkdata/300_ap_3000_total_random_input"
    dataset = CDictDataset()
    dataset.load_data(input_file)

    b = AsyncBackTracker(dataset, register_result)

    b.search()



