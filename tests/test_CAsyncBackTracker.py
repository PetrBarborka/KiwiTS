import unittest

import sys, os
sys.path.append(os.path.realpath(".."))
sys.path.append(os.path.realpath("../src"))

from src.searchers.CAsyncBackTracker import CAsyncBackTracker
from src.datasets import DataPath

import logging, datetime

ts = datetime.datetime.now().strftime("%d-%m-%Y-%I-%M%p")
lfile = "../logs/tests/{}BackTrackerLookup_test.log".format(ts)

log_to_file = True
log_to_console = not log_to_file

fmt = '%(relativeCreated)dms %(module)s %(funcName)s %(levelname)-8s \n\t%(message)s'
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

# logging.disable(logging.CRITICAL)
# logger_interface = logging.getLogger("GeneralBackTrackerInterface")
# logger_interface.setLevel(level=logging.CRITICAL)
# logger_interface.propagate = False

def load_data(path):
    from src.datasets.CDictDataset import CDictDataset
    d = CDictDataset()
    # d.load_data('input/3_airports_input.csv')
    # d.load_data('../input/3_airports_backtrace.csv')
    d.load_data(path)
    return d

def register_result_callback(path):
    assert path.is_valid()
    print( "found path for: {}:\n{} ".format(path.price, path) )
    # print( "found path for: {}".format(path.price) )

def best_result_callback():
    # print( "best_path callback called" )
    return None

class BackTrackerLookupTest(unittest.TestCase):

    def test_5ap(self):

        dataset = load_data('../input/5_airports.csv')

        print("async")
        async = CAsyncBackTracker(dataset, register_result_callback, best_result_callback)
        p =  async.search()

    def test_big_from_to(self):

        dataset = load_data('../input/300_90K_flights.csv')
        
        # print("async")
        async = CAsyncBackTracker(dataset, register_result_callback, best_result_callback)
        p =  async.search()

        # self.assertTrue( p.is_valid() )

if __name__ == '__main__':
    unittest.main()
