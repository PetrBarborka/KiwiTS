from copy import deepcopy
import sys, os
sys.path.append(os.path.realpath(".."))

# from datasets.DataPath import DataPath
from datasets.DataPath import DataPath

import logging

class GeneralBackTrackerInterface:

    def __init__(self, dataset, register_result_callback):
        self.dataset = dataset
        # self.register_result = register_result_callback
        # self.best_price_so_far = None

    def search(self):
        raise NotImplementedError( "Should have implemented this" )

    def _from_to(self, cities_to_visit, day1, day2, ap1, ap2):
        """Get the best path (brutefoce) from ap1 day1 to ap2 day2"""
        if day1 > day2:
            raise ValueError( "day2 has to be >= day1" )

        logging.debug("STARTING THE METHOD from {}, day {} to {}, day {}"\
                     .format(ap1, day1, ap2, day2) )

        result_path = None

        assert day2 > day1

        cities_to_visit = deepcopy(cities_to_visit)
        if ap1 in cities_to_visit :
            cities_to_visit.remove(ap1) 
        if ap2 in cities_to_visit :
            cities_to_visit.remove(ap2) 

        path = DataPath()
        logging.debug( "Path after construction: {}".format(path) )
        assert path.flights == [] and path.price == 0
        #possible_flights = { day : [flight flight flight ... ] }
        # je to vpodstate stack
        possible_flights = {}

        # best price for this execution of this function
        local_best_price = None

        day = day1
        cur_city = ap1

        while True:
            if day not in possible_flights.keys():
                possible_flights[day] = \
                    self.dataset.get_flights(cur_city,
                                             day,
                                             cities_to_visit=cities_to_visit,
                                             sort_by_price=True)

            flights_are_available = True if possible_flights[day] else False
            price_is_not_too_high = flights_are_available and \
                                    ( (local_best_price is None) or \
                                      path.price + \
                                      possible_flights[day][0].price < \
                                      local_best_price )

            logging.debug( "path: {}\n\tpossible flights: {}\n\tbest price so far: {}"\
                          .format(path, possible_flights[day], 
                                  local_best_price) )

            if flights_are_available and price_is_not_too_high:
                #forward

                flight_taken = possible_flights[day].pop(0)
                path.push_flight(flight_taken)

                cities_to_visit.remove(flight_taken.city_to)
                cur_city = flight_taken.city_to

                day += 1
                logging.debug( "Taking flight {}".format(flight_taken) )

            elif day < day2 - 1:
                #backwards

                logging.debug( "backtracking ..." )

                if day == day1:
                    logging.debug( "self.dataset exhausted, returning" )
                    return result_path

                del possible_flights[day]

                last_flight = path.pop_flight()

                cities_to_visit.append(cur_city)
                cur_city = last_flight.city_from

                day -= 1

            # finish on the right city:
            if day == (day2 - 1):
                return_possibilities = \
                        self.dataset.get_flights( cur_city,
                                                  day,
                                                  cities_to_visit=[ap2],
                                                  sort_by_price=True )

                flights_are_available = True if return_possibilities else False
                price_is_not_too_high = flights_are_available and \
                                        ( (local_best_price is None) or \
                                        path.price + \
                                        return_possibilities[0].price < \
                                        local_best_price )

                logging.debug( "day: {}, looking for a flight back to {}"\
                                .format(day, ap2) )
                logging.debug( "path: {}\n\tpossible return flights: {}\n\tbest price so far: {}"\
                          .format(path, return_possibilities, local_best_price) )

                if flights_are_available and price_is_not_too_high:

                    flight_taken = return_possibilities.pop(0)
                    path.push_flight(flight_taken)

                    if path.is_valid(partial=True):
                        local_best_price = path.price
                    else: 
                        logging.error( "found invalid path, has to be a BUG" )
                        assert False, "should not compute invalid path"

                    logging.debug( "FOUND NEW BEST PATH: \n\t{}, returning".format(path) )
                    return path
                    logging.error( "after return??? rly??" )

                    result_path = path.copy()

                    path.pop_flight()

                logging.debug( "backtracking ..." )
                last_flight = path.pop_flight()
                cities_to_visit.append(cur_city)
                cur_city = last_flight.city_from
                day -= 1
                assert day >= day1, "bug: returning before day 0"

    def __from_steps_forwards(cities_to_visit, days, day1, ap1):
        """Get the best path (brutefoce) from ap1 day1 for a given
           number of days."""

        raise NotImplementedError( "Should have implemented this" )


if __name__ == "__main__":

    def register_result(path):
        validity = "VALID" if path.is_valid() else "NON-VALID"
        print( "found {} path for: {}".format( validity, path.price ) )

    import sys, os
    sys.path.append(os.path.realpath(".."))
    from datasets.CDictDataset import CDictDataset

    # input_file = "../../benchmark/benchmarkdata/300_ap_3000_total_random_input"
    input_file = "../../kiwisources/travelling-salesman/real_data/data_300.txt"
    dataset = CDictDataset()
    dataset.load_data(input_file)

    b = AsyncBackTracker(dataset, register_result)

    b.search()



