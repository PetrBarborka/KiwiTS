from copy import deepcopy
import sys, os
sys.path.append(os.path.realpath(".."))

# from datasets.DataPath import DataPath
from datasets.DataPath import DataPath

import logging

class GeneralBackTrackerInterface:

    def __init__(self, dataset, register_result_callback):
        self.dataset = dataset
        self.register_result = register_result_callback

    def search(self):
        raise NotImplementedError( "Should have implemented this" )

    def _from_to(self, cities_to_visit, day1, day2, ap1, ap2):
        """Get the best path (brutefoce) from ap1 day1 to ap2 day2"""
        if day1 > day2:
            raise ValueError( "day2 has to be >= day1" )
        elif day2 - day1 == 1:
            flights = self.dataset.get_flights( ap1,
                                                day1,
                                                cities_to_visit=[ap2],
                                                sort_by_price=True)
            if flights:
                return DataPath([flights[0]], flights[0].price)
            else:
                return None


        dstr = 100 * "=" + "\n"
        dstr += "STARTING THE METHOD from {}, day {} to {}, day {}"
        logging.debug(dstr.format(ap1, day1, ap2, day2) )

        result_path = None

        assert day2 > day1

        cities_to_visit = deepcopy(cities_to_visit)
        if ap1 in cities_to_visit :
            cities_to_visit.remove(ap1) 
        if ap2 in cities_to_visit :
            cities_to_visit.remove(ap2) 

        path = DataPath()
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
                assert day >= day1
                c = cities_to_visit if day < (day2 - 1) else [ap2]
                possible_flights[day] = \
                    self.dataset.get_flights(cur_city,
                                             day,
                                             cities_to_visit=c,
                                             sort_by_price=True)

            flights_are_available = True if possible_flights[day] else False
            price_is_not_too_high = flights_are_available and \
                                    ( (local_best_price is None) or \
                                      path.price + \
                                      possible_flights[day][0].price < \
                                      local_best_price )

            logging.debug( "day: {},path: {}\n\tpossible flights: {}\n\tbest price so far: {}"\
                          .format(day, path, possible_flights[day], 
                                  local_best_price) )

            if flights_are_available and price_is_not_too_high:
                #forward
                dstr = ""

                if day == (day2 - 1):
                    dstr = "day: {}, looking for a flight back to {}\n".format(day, ap2)
                    dstr += "path: {}\n\tpossible return flights: {}\n\tbest price so far: {}\n"\
                            .format(path, possible_flights[day], local_best_price)

                flight_taken = possible_flights[day].pop(0)
                path.push_flight(flight_taken)

                dstr += "Taking flight {}".format(flight_taken)
                logging.debug( dstr )

                if day == (day2 - 1):

                    if path.is_valid(partial=True):
                        local_best_price = path.price
                    else: 
                        logging.error( "found invalid path, has to be a BUG" )
                        assert False, "should not compute invalid path"

                    logging.debug( "FOUND NEW BEST PATH: \n\t{}".format(path) )

                    result_path = path.copy()

                    path.pop_flight() # returning point
                    path.pop_flight() # one more

                    del possible_flights[day]
                    day -= 1

                else:
                    cities_to_visit.remove(flight_taken.city_to)
                    cur_city = flight_taken.city_to

                    day += 1

            else :
                #backwards

                dstr = "backtracking ... "

                if day == day1:
                    dstr += "self.dataset exhausted, returning \n"
                    dstr += "result_path: \n\t{}".format(result_path)
                    logging.debug(dstr)
                    return result_path

                logging.debug(dstr)

                del possible_flights[day]

                last_flight = path.pop_flight()

                cities_to_visit.append(cur_city)
                cur_city = last_flight.city_from

                day -= 1

    def _from_days_forward(self, cities_to_visit, num_days, day1, ap1):
        """Get the best path (brutefoce) from ap1 day1 for a given
           number of days."""
        assert num_days > 0
        if num_days == 1:
            flights = self.dataset.get_flights( ap1,
                                                day1,
                                                cities_to_visit=cities_to_visit,
                                                sort_by_price=True)
            if flights:
                out = []
                for f in flights:
                    if not f.city_to == ap1:
                        out.append(DataPath([f], f.price))
                return sorted(out, key=lambda x: x.price)
            else:
                return None


        dstr = 100 * "=" + "\n"
        dstr += "STARTING THE METHOD from {}, day {} best for {} days"
        logging.debug( dstr.format(ap1, day1, num_days) )

        result_paths = None

        cities_to_visit = deepcopy(cities_to_visit)
        if ap1 in cities_to_visit :
            cities_to_visit.remove(ap1) 

        path = DataPath()
        assert path.flights == [] and path.price == 0
        #possible_flights = { day : [flight flight flight ... ] }
        # je to vpodstate stack
        possible_flights = {}

        day = day1
        cur_city = ap1

        while True:
            if day not in possible_flights.keys():
                assert day >= day1
                possible_flights[day] = \
                    self.dataset.get_flights(cur_city,
                                             day,
                                             cities_to_visit=cities_to_visit,
                                             sort_by_price=True)


            logging.debug( "day: {}, city: {}, path: {}\n\tpossible flights: {}"\
                          .format(day, cur_city, path, possible_flights[day]) )

            if possible_flights[day]:
                #forward
                dstr = ""

                flight_taken = possible_flights[day].pop(0)
                path.push_flight(flight_taken)

                dstr += "Taking flight {}".format(flight_taken)
                logging.debug( dstr )

                if day == (day1 + num_days - 1):

                    if not path.is_valid(partial=True):
                        logging.error( "found invalid path, has to be a BUG" )
                        assert False, "should not compute invalid path"

                    logging.debug( "FOUND NEW PATH: \n\t{}".format(path) )

                    if result_paths is not None:
                        result_paths.append( path.copy() )
                    else:
                        result_paths = [path.copy()]

                    path.pop_flight() # returning point

                else:
                    cities_to_visit.remove(flight_taken.city_to)
                    cur_city = flight_taken.city_to

                    day += 1

            else :
                #backwards

                dstr = "backtracking ... "

                if day == day1:
                    dstr += "self.dataset exhausted, returning \n"
                    dstr += "result_paths: \n\t{}".format(result_paths)
                    logging.debug(dstr)
                    if result_paths:
                        return sorted(result_paths, key=lambda p: p.price)
                    else:
                        return None

                logging.debug(dstr)

                del possible_flights[day]

                last_flight = path.pop_flight()

                cities_to_visit.append(cur_city)
                cur_city = last_flight.city_from

                day -= 1


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



