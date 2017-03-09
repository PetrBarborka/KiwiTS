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

import datetime

import logging

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

        if any_alive(threads):
            logging.info("some threads are still alive after timeout of {}s"
                         .format(timeout) )
        else:
            logging.info("all threads finished before timeout of {}s"
                         .format(timeout) )

        # self.final_report()

    def register_result(self, path, method_name="method name undefined"):
        # assert isinstance(path, DataPath), \
               # "{}: Na takový extrabuřty tady nejsme vedený!".format(path.__class__.__name__)

        validity = "VALID" if path.is_valid() else "NON-VALID"
        td = timer() - self.time_start
        logging.info( "{} found {} path for {}"
                      .format( method_name, validity, path.price ) )

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
    # input_file = 'benchmark/benchmarkdata/300_ap_1500000_total_random_input'
    # input_file = 'benchmark/benchmarkdata/300_ap_3000_total_random_input'
    input_file = "kiwisources/travelling-salesman/real_data/data_300.txt"
    # input_file = "kiwisources/travelling-salesman/real_data/sorted_data/data_100.txt"
    # input_file = "kiwisources/travelling-salesman/real_data/sorted_data/data_200.txt"
    # input_file = "kiwisources/travelling-salesman/real_data/sorted_data/data_30.txt"

    ts = datetime.datetime.now().strftime("%d-%m-%Y-%I-%M%p")
    lfile = "logs/{}_{}AsyncManager.log".format(input_file.split('.')[0].split('/')[-1], ts)

    log_to_file = True
    log_to_console = not log_to_file

    fmt = '%(relativeCreated)dms %(module)s %(funcName)s %(levelname)-8s %(message)s'
    if log_to_file:
        logging.basicConfig(filename=lfile, 
                            format=fmt,
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout,
                            format=fmt,
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
    logging.info("loading input file {} ...".format(input_file) )
    dataset.load_data(input_file)
    logging.info("done")
    
    timeout = 120
    AM = AsyncManager(dataset, [AsyncBackTracker])
    p = Process(target=partial(AM.search_async, timeout=(timeout - 1)))

    logging.info("starting AsyncManager process")
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        logging.info("Async manager process timed out")
    else:
        logging.info("Async manager process ended")
