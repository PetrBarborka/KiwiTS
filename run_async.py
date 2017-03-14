# import multiprocessing as mp
from multiprocessing import Process
from threading import Thread, Lock
from functools import partial

from copy import deepcopy

from timeit import default_timer as timer
import time

import sys, os
sys.path.append(os.path.realpath("src"))

from src.datasets import CDictDataset
from src.searchers import BackTracker
from src.searchers import ShortestPath
from src.searchers import Tribe
from src.searchers.AsyncBackTracker import AsyncBackTracker
from src.searchers.BackTrackerLookup import BackTrackerLookup

import datetime

import logging

class AsyncManager:
    def __init__(self, dataset, search_fcns):
        self.dataset = dataset
        self.search_fcns = search_fcns
        self.best_result = None
        # {
        # (price, path) :
            # [ [(method, timefound), 
            # (method2, timefound2) ... ]
             # ... ] 
        # }
        self.results = None
        self.time_start = None
        self.result_lock = Lock()

    def search_async(self, timeout=30):

        def any_alive(threads):
            o = [t.name for t in threads if t.is_alive()]
            if o:
                return o
            else:
                return None

        threads = []
        for f in self.search_fcns:
            t = Thread(target=f, name=str(f))
            threads.append(t)
        logging.info( "{} workers".format(len(threads)) )
        self.time_start = timer()
        for t in threads:
            t.start()

        while( timer() - self.time_start < timeout and any_alive(threads) ):
            time.sleep(1)

        alive = any_alive(threads)
        if alive:
            logging.info("some threads are still alive after timeout of {}s"
                         .format(timeout) )
            # logging.info("threads {} are still alive after timeout of {}s"
                         # .format(alive, timeout) )
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
            with self.result_lock:
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

    def get_best_result(self):
        with self.result_lock:
            if self.best_result:
                return self.best_result["path"]
            else:
                return None

if __name__ == '__main__':

    ts = datetime.datetime.now().strftime("%d-%m-%Y-%I-%M%p")
    # lfile = "logs/{}_{}AsyncManager.log".format(input_file.split('.')[0].split('/')[-1], ts)
    lfile = "logs/multifile_{}AsyncManager.log".format(ts)

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

    def do_file(input_file, timeout):
        dataset = CDictDataset()
        logging.info("=" * 50 )
        logging.info("loading input file {} ...".format(input_file) )
        dataset.load_data(input_file)
        logging.info("done")
        
        AM = AsyncManager(dataset, [])
        set_result_callback = partial( AM.register_result, method_name="Simple backtracker" )
        get_result_callback = AM.get_best_result
        # search_fcns = [AsyncBackTracker(dataset.copy(), set_result_callback, get_result_callback).search]
        search_fcns = []
        # lookups = [1,2,3,5,10,15,30]
        lookups = [1,2,3]
        # steps = [1,2,3,5,10,15,30]
        steps = [1,2]
        for ls in [(1,1), (2,1), (3,2)]:
            lookup=ls[0]
            step=ls[1]
            set_result_callback = partial( AM.register_result, method_name="Lookup_l:{}_s:{}".format(lookup, step) )
            search_fcns.append(partial(BackTrackerLookup(dataset, set_result_callback,
                                                            get_result_callback).search, lookup, step))
        AM.search_fcns = search_fcns

        wrap_in_process = True # turn false for pycharm concurrency to see the threads
        if wrap_in_process:
            p = Process(target=partial(AM.search_async, timeout=(timeout - 1)))

            logging.info("starting AsyncManager process")
            p.start()
            p.join(timeout)
            if p.is_alive():
                p.terminate()
                logging.info("Async manager process timed out")
            else:
                logging.info("Async manager process ended")
        else:
            AM.search_async(timeout=timeout-2)

    files = []
    # input_file = 'benchmark/benchmarkdata/300_ap_1500000_total_random_input'
    # input_file = 'benchmark/benchmarkdata/300_ap_3000_total_random_input'
    # input_file = "kiwisources/travelling-salesman/real_data/data_300.txt"
    # input_file = "kiwisources/travelling-salesman/real_data/sorted_data/data_100.txt"
    # input_file = "kiwisources/travelling-salesman/real_data/sorted_data/data_200.txt"
    # files.append("kiwisources/travelling-salesman/real_data/sorted_data/data_5.txt")
    # files.append("kiwisources/travelling-salesman/real_data/sorted_data/data_15.txt")
    # files.append("kiwisources/travelling-salesman/real_data/sorted_data/data_30.txt")
    # files.append("kiwisources/travelling-salesman/real_data/sorted_data/data_50.txt")
    # files.append("kiwisources/travelling-salesman/real_data/sorted_data/data_100.txt")
    # files.append("kiwisources/travelling-salesman/real_data/sorted_data/data_200.txt")
    files.append("kiwisources/travelling-salesman/real_data/data_300.txt")

    timeout = 30
    for f in files:
        do_file(f, timeout)
