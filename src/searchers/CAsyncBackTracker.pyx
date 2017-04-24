from copy import deepcopy
import sys, os
sys.path.append(os.path.realpath(".."))

from datasets import DataPath

import logging

class CAsyncBackTracker:
    """ A simple backtracking algorithm augmented with a very basic
        branch cutting """

    def __init__(self, dataset, register_result_callback, best_result_callback):
        self.dataset = dataset
        self.register_result = register_result_callback
        self.best_result_callback = best_result_callback
        self.best_price_so_far = None

    def search(self):

        path = DataPath()
        #possible_flights = { day : [flight flight flight ... ] }
        # je to vpodstate stack
        possible_flights = {}

        start_city = self.dataset.get_starting_city()
        cities_to_visit = deepcopy(self.dataset.cities)
        cities_to_visit.remove(start_city)

        cdef int day = 0
        cur_city = start_city

        while(cities_to_visit):
            if day not in possible_flights.keys():
                possible_flights[day] = \
                        self.dataset.get_flights(cur_city,
                                                 day,
                                                 cities_to_visit=cities_to_visit,
                                                 sort_by_price=True)

            flights_are_available = True if possible_flights[day] else False
            price_is_not_too_high = flights_are_available and \
                                    ( (self.best_price_so_far is None) or \
                                      path.price + possible_flights[day][0].price < \
                                      self.best_price_so_far )

            if flights_are_available and price_is_not_too_high:
                #forward

                flight_taken = possible_flights[day].pop(0)
                path.push_flight(flight_taken)

                cities_to_visit.remove(flight_taken.city_to)
                cur_city = flight_taken.city_to

                day += 1

            else:
                #backwards

                if day == 0:
                    logging.info( "self.dataset exhausted" )
                    return

                del possible_flights[day]

                last_flight = path.pop_flight()

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

                flights_are_available = True if return_possibilities else False
                global_best = self.best_result_callback()
                if global_best:
                    self.best_price_so_far = global_best.price
                price_is_not_too_high = flights_are_available and \
                                        ( (self.best_price_so_far is None) or \
                                        path.price + return_possibilities[0].price < \
                                        self.best_price_so_far )
                if flights_are_available and price_is_not_too_high:

                    flight_taken = return_possibilities.pop(0)
                    path.push_flight(flight_taken)

                    if path.is_valid():
                        self.best_price_so_far = path.price
                        # print ( "best price so far: {}".format(self.best_price_so_far) )

                    self.register_result( path )

                    path.pop_flight()

                last_flight = path.pop_flight()
                cities_to_visit.append(cur_city)
                cur_city = last_flight.city_from
                day -= 1
                assert day >= 0, "bug: returning before day 0"
