# import multiprocessing as mp
from multiprocessing import Process
from threading import Thread
from functools import partial

from timeit import default_timer as timer
import time

import sys, os
sys.path.append(os.path.realpath("src"))

from src.datasets import CDictDataset
from src.searchers import BackTracker
from src.searchers import ShortestPath
from src.searchers import Tribe
from src.searchers.AsyncBackTracker import AsyncBackTracker


class AsyncManager:
    def __init__(self, dataset, searchers):
        self.dataset = dataset
        self.searchers = searchers
        self.best_result = None
        # {
        # (price, path) :
            # [ [(method, timefound), 
            # (method2, timefound2) ... ]
             # ... ] 
        # }
        self.results = None
        self.time_start = None

    def search_async(self, timeout=30):

        def any_alive(threads):
            alive = True
            for t in threads:
                alive = alive and t.is_alive() 
            return alive

        threads = []
        for s in self.searchers:
            callback = partial(self.register_result,
                               method_name=s.__name__ )
            searcher_instance = s(self.dataset, callback)
            t = Thread(target=searcher_instance.search)
            threads.append(t)
        self.time_start = timer()
        for t in threads:
            t.start()

        while( timer() - self.time_start < timeout and any_alive(threads) ):
            time.sleep(1)

        # self.final_report()

    def register_result(self, path, method_name="method name undefined"):
        # assert isinstance(path, DataPath), \
               # "{}: Na takový extrabuřty tady nejsme vedený!".format(path.__class__.__name__)

        validity = "VALID" if path.is_valid() else "NON-VALID"
        td = timer() - self.time_start
        print( "{} found {} path for: {}\n\ton: {}"
              .format( method_name, validity, path.price, td ) )

        if path.is_valid():
            if self.best_result is None or self.best_result["path"].price > path.price:
                self.best_result = {"path": path,
                                    "time": td,
                                    "method": method_name }

            try:
                self.results[(path.price, path)].append((method_name, td))
            except KeyError:
                self.results[(path.price, path)] = [(method_name, td)]
            except TypeError:
                self.results = {(path.price, path): [(method_name, td)] }

    def log_result(self, searcher_name, time_taken, path):
        cost = sum(p.price for p in path)
        print('-' * 100)
        print('Search complete:')
        print('\t{:15}{}'.format('Searcher:', searcher_name))
        print('\t{:15}{}s'.format('Run time:', round(time_taken, 5)))
        print('\t{:15}{}'.format('Cost:', cost))
        print('\t{:15}{}'.format('Path:', path))

if __name__ == '__main__':
    dataset = CDictDataset()
    # d.load_data('benchmark/benchmarkdata/300_ap_1500000_total_random_input')
    # dataset.load_data('benchmark/benchmarkdata/300_ap_3000_total_random_input')
    # dataset.load_data("kiwisources/travelling-salesman/real_data/data_300.txt")
    # dataset.load_data("kiwisources/travelling-salesman/real_data/sorted_data/data_100.txt")
    # dataset.load_data("kiwisources/travelling-salesman/real_data/sorted_data/data_200.txt")
    dataset.load_data("kiwisources/travelling-salesman/real_data/sorted_data/data_30.txt")
    
    timeout = 30
    AM = AsyncManager(dataset, [AsyncBackTracker])
    p = Process(target=partial(AM.search_async, timeout=timeout))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        print("Async manager process timed out")
