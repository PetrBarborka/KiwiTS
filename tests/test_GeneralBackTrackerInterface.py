import unittest

import sys, os
sys.path.append(os.path.realpath(".."))
sys.path.append(os.path.realpath("../src"))

from src.searchers.GeneralBackTrackerInterface import GeneralBackTrackerInterface
# from src.searchers.GeneralBackTrackerInterface import __from_to_forwards
from src.datasets import CFlight
from src.datasets import DataPath

import logging, datetime

ts = datetime.datetime.now().strftime("%d-%m-%Y-%I-%M%p")
lfile = "../logs/tests/{}GeneralBackTrackerInterface_test.log".format(ts)

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

def load_data(path):
    from src.datasets.CDictDataset import CDictDataset
    d = CDictDataset()
    # d.load_data('input/3_airports_input.csv')
    # d.load_data('../input/3_airports_backtrace.csv')
    d.load_data(path)
    return d

def register_result_callback(path):
    print( "register_result_callback should not be called! " )

class DataPathTest(unittest.TestCase):

    def test_constructor(self):

        d = DataPath()
        self.assertEqual(d.price, 0)
        self.assertEqual(d.flights, [])

        f = [CFlight("PRG", "BCN", 0, 0)]
        d = DataPath(f, 0)
        self.assertEqual(d.price, 0)
        self.assertEqual(d.flights, f)

        d = DataPath()
        self.assertEqual(d.price, 0)
        self.assertEqual(d.flights, [])

class BacktracerTest(unittest.TestCase):

    def test_3ap_from_to(self):

        dataset = load_data('../input/3_airports_backtrace.csv')

        b = GeneralBackTrackerInterface(dataset, register_result_callback)

        p =  b._from_to(["PRG", "BCN", "TXL"], 0, 3, "PRG", "PRG")
        self.assertEqual(p.flights[0], CFlight("PRG", "TXL", 0, 100))
        self.assertEqual(p.flights[1], CFlight("TXL", "BCN", 1, 100))
        self.assertEqual(p.flights[2], CFlight("BCN", "PRG", 2, 100))

        p =  b._from_to(["PRG", "BCN"], 0, 1, "PRG", "BCN")
        self.assertEqual(p.flights[0], CFlight("PRG", "BCN", 0, 50))

        p =  b._from_to(["BCN", "TXL"], 1, 2, "BCN", "TXL")
        self.assertEqual(p.flights[0], CFlight("BCN", "TXL", 1, 20))
        
        p =  b._from_to(["PRG", "BCN", "TXL"], 1, 3, "BCN", "PRG")
        self.assertEqual(p, None)

        p =  b._from_to(["PRG", "BCN", "TXL"], 1, 3, "TXL", "PRG")
        self.assertEqual(p.flights[0], CFlight("TXL", "BCN", 1, 100))
        self.assertEqual(p.flights[1], CFlight("BCN", "PRG", 2, 100))

        p =  b._from_to(["PRG", "BCN", "TXL"], 0, 2, "PRG", "TXL")
        self.assertEqual(p.flights[0], CFlight("PRG", "BCN", 0, 50))
        self.assertEqual(p.flights[1], CFlight("BCN", "TXL", 1, 20))

    def test_big_from_to(self):

        dataset = load_data('../input/300_90K_flights.csv')
        b = GeneralBackTrackerInterface(dataset, register_result_callback)

        p =  b._from_to(dataset.cities, 0, 300, 
                        dataset.get_starting_city(), dataset.get_starting_city() )

        self.assertTrue( p.is_valid() )

    def test_3ap_from_days_forward(self):

        dataset = load_data('../input/3_airports_backtrace.csv')

        b = GeneralBackTrackerInterface(dataset, register_result_callback)

        p =  b._from_days_forward(["PRG", "BCN", "TXL"], 2, 0, "PRG")
        self.assertEqual(p.flights[0], CFlight("PRG", "BCN", 0, 50))
        self.assertEqual(p.flights[1], CFlight("BCN", "TXL", 1, 20))

        p =  b._from_days_forward(["PRG", "BCN", "TXL"], 2, 1, "BCN")
        self.assertEqual(p.flights[0], CFlight("BCN", "PRG", 1, 30))
        self.assertEqual(p.flights[1], CFlight("PRG", "TXL", 2, 30))

    def test_big_from_to(self):

        dataset = load_data('../input/300_90K_flights.csv')
        b = GeneralBackTrackerInterface(dataset, register_result_callback)

        p =  b._from_days_forward(dataset.cities, 299, 0, 
                        dataset.get_starting_city() )

        self.assertTrue( p.is_valid(partial=True) )

if __name__ == '__main__':
    unittest.main()
