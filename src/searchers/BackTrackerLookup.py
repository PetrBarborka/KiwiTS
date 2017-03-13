from copy import deepcopy
import sys, os
sys.path.append(os.path.realpath(".."))

# from datasets.DataPath import DataPath
from datasets.DataPath import DataPath
from .GeneralBackTrackerInterface import GeneralBackTrackerInterface
import logging

class BackTrackerLookup(GeneralBackTrackerInterface):

    def __init__(self, dataset, register_result_callback, best_result_callback):
        super(BackTrackerLookup, self).__init__(dataset,
                                                register_result_callback,
                                                best_result_callback)
        self.best_path = None

    def search(self, lookup, step):
        """ find valid path each time bruteforcing "lookup" next flights
            and then using first "step" of them. 1 and 1 gives you 
            classic backtracking bruteforcer """

        def backwards(day, city, step, path, cities_to_visit, possible_paths):
            # logging.debug( "backtracking from day {} ... \n".format(day) )
            # go back given ammount of steps
            for i in range(step):
                f = path.pop_flight()
                cities_to_visit.append(f.city_to)
            if len(path.flights) > 0:
                city = path.flights[-1].city_to
            else:
                city = self.dataset.get_starting_city()
            day -= step

            return day, city, path, cities_to_visit, possible_paths

        def forwards(day, city, step, path, cities_to_visit, possible_paths):
            # logging.debug("going forwards ... \n")
            # go forward given ammount of steps
            path_taken = possible_paths[day].pop(0)
            for i in range(step):
                f = path_taken.flights[i]
                path.push_flight(f)
                cities_to_visit.remove(f.city_to)
            city = path.flights[-1].city_to
            day += step

            return day, city, path, cities_to_visit, possible_paths

        def return_to_target(day, final_day, city, cities_to_visit, path, destination):
            # logging.debug( "returning to {} ".format(destination) )
            # find path from here to starting city:
            best_return = self._from_to(  cities_to_visit,
                                          day,
                                          final_day,
                                          city,
                                          destination  )

            dstr = "day: {}, city: {}, price: {}, path:\n{},"
            # logging.debug( dstr.format(day, city, path.price, path) )
            # logging.debug( "return path: {}".format(best_return) )
            if best_return:
                best_path = path.copy()
                for f in best_return.flights:
                    best_path.push_flight(f)
                global_best = self.best_result_callback()
                if global_best:
                    self.best_path = global_best
                price_is_too_high = self.best_path is not None and\
                                    best_path.price >= self.best_path.price
                if price_is_too_high:
                    best_path = None
                return best_path
            else:
                return None

        assert lookup > 0 and step > 0
        assert lookup >= step

        dstr = 100 * "=" + "\n"
        dstr += "STARTING THE METHOD lookup: {}, step: {}".format(lookup,step)
        # logging.debug( dstr )

        cities_to_visit = deepcopy(self.dataset.cities)
        final_day = len(cities_to_visit)
        cities_to_visit.remove(self.dataset.get_starting_city())

        day = 0
        city = self.dataset.get_starting_city()

        path = DataPath()

        possible_paths = {}

        while True:
            assert day >= 0

            if day + lookup >= final_day:
                dstr = "day + lookup = {} + {} = {},\n".format(day, lookup, day+lookup)
                dstr += "final_day is {}.bruteforcing my way back.".format(final_day)
                # logging.debug(dstr)

                destination = self.dataset.get_starting_city()
                solution = return_to_target(day, final_day, city,
                                            cities_to_visit, path, destination)
                if solution is not None:
                    assert solution.is_valid()
                    self.best_path = solution
                    self.register_result(solution)
                    dstr = 50 * "- " + "\n"
                    dstr += "FOUND NEW SOLUTION: {}".format(solution)
                    # logging.debug( dstr )

                if day > 0:
                    day -= 1
                    day, city, path, cities_to_visit, possible_paths = \
                        backwards(day, city, step, path, cities_to_visit, possible_paths)
                    day += 1
                else:
                    return self.best_path

            if day not in possible_paths.keys():
                possible_paths[day] = self._from_days_forward(  cities_to_visit,
                                                                num_days=lookup,
                                                                day1=day,
                                                                ap1=city  )

            # logging.debug( "possible paths: {}".format(possible_paths) )
            dstr = "day: {}, city: {}, price: {}, path:\n{},\npossibilities:\n{}"\
                    .format(day, city, path.price, path, possible_paths[day])
            dstr += "\n\tcities_to_visit: \n\t{}".format(cities_to_visit)
            # logging.debug( dstr )

            flights_are_available = True if possible_paths[day] else False

            if flights_are_available:
                potential_price = path.price +  \
                                  sum([possible_paths[day][0].flights[i].price for i in range(step)])
                price_is_not_too_high = self.best_path is None or \
                                        potential_price < self.best_path.price

            if flights_are_available and price_is_not_too_high:

                day, city, path, cities_to_visit, possible_paths = \
                    forwards(day, city, step, path, cities_to_visit, possible_paths)

            else:

                if day == 0:
                    # logging.debug( "dataset exhausted" )
                    return self.best_path

                del possible_paths[day]
                day, city, path, cities_to_visit, possible_paths = \
                    backwards(day, city, step, path, cities_to_visit, possible_paths)


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



