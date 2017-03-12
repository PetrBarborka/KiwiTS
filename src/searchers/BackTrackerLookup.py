from copy import deepcopy
import sys, os
sys.path.append(os.path.realpath(".."))

# from datasets.DataPath import DataPath
from datasets.DataPath import DataPath
from .GeneralBackTrackerInterface import GeneralBackTrackerInterface
import logging

class BackTrackerLookup(GeneralBackTrackerInterface):

    def __init__(self, dataset, register_result_callback):
        super(BackTrackerLookup, self).__init__(dataset, register_result_callback)
        self.best_path = None

    def search(self, lookup, step):
        """ find valid path each time bruteforcing "lookup" next flights
            and then using first "step" of them. 1 and 1 gives you 
            classic backtracking bruteforcer """
        assert lookup > 0 and step > 0
        assert lookup >= step

        dstr = 100 * "=" + "\n"
        dstr += "STARTING THE METHOD"
        logging.debug( dstr )

        cities_to_visit = deepcopy(self.dataset.cities)
        final_day = len(cities_to_visit)
        cities_to_visit.remove(self.dataset.get_starting_city())

        day = 0
        city = self.dataset.get_starting_city()

        path = DataPath()

        possible_paths = {}

        while True:
            assert day >= 0

            if day + lookup < final_day:

                if day not in possible_paths.keys():
                    possible_paths[day] = self._from_days_forward(  cities_to_visit,
                                                                    num_days=lookup,
                                                                    day1=day,
                                                                    ap1=city  )

                dstr = "day: {}, city: {}, price: {}, path:\n{},\npossibilities:\n{}"
                logging.debug( dstr.format(day, city, path.price, 
                                        path, possible_paths[day]) )

                if possible_paths[day]:

                    # go forward given ammount of steps
                    path_taken = possible_paths[day].pop(0)
                    logging.debug( "path taken: {}".format(path_taken) )
                    for i in range(step):
                        f = path_taken.flights[i]
                        path.push_flight(f)
                        cities_to_visit.remove(f.city_to)
                    city = path.flights[-1].city_to
                    day += step

                else:

                    if day == 0:
                        return self.best_path

                    # go back given ammount of steps
                    for i in range(step):
                        f = path.pop_flight()
                        cities_to_visit.append(f.city_to)
                    if len(path.flights) > 0:
                        city = path.flights[-1].city_to
                    else:
                        city = self.dataset.get_starting_city()

                    del possible_paths[day]

                    day -= step

            if day + lookup >= final_day:
                dstr = "day + step = {} + {} = {},\n".format(day, step, day+step)
                dstr += "final_day is {}.bruteforcing my way back."\
                        .format(final_day)
                logging.debug(dstr)
                start = self.dataset.get_starting_city()
                # find path from here to starting city:
                best_return = self._from_to(  cities_to_visit,
                                              day,
                                              final_day,
                                              city,
                                              start  )

                dstr = "day: {}, city: {}, price: {}, path:\n{},"
                logging.debug( dstr.format(day, city, path.price, path) )
                logging.debug( "return path: {}".format(best_return) )
                if best_return:
                    self.best_path = path.copy()
                    for f in best_return.flights:
                        self.best_path.push_flight(f)
                    assert self.best_path.is_valid()
                    self.register_result(self.best_path)

                # go back given ammount of steps
                if day == 0:
                    return self.best_path
                for i in range(step):
                    f = path.pop_flight()
                    cities_to_visit.append(f.city_to)
                day -= step
                if day > 0:
                    city = path.flights[-1].city_to
                else:
                    city = self.dataset.get_starting_city()



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



