import unittest

import sys, os
sys.path.append(os.path.realpath(".."))

from timeit import timeit
from functools import partial

import numpy as np

from src.datasets import MatrixDataset
from src.datasets import CFlight

class MatrixDatasetTest(unittest.TestCase):

    def test_cities(self):
        d = MatrixDataset()
        d.load_data('../input/3_airports_backtrace.csv')

        self.assertTrue("PRG" in d.cities )
        self.assertTrue("TXL" in d.cities )
        self.assertTrue("TXL" in d.cities )

    def test_flights(self):
        d = MatrixDataset()
        d.load_data('../input/3_airports_backtrace.csv')

        self.assertEqual(CFlight("PRG", "TXL", 0, 100), d.get_flight_by_id(0))
        self.assertEqual(CFlight("BCN", "TXL", 1, 20), d.get_flight_by_id(4))
        self.assertEqual(CFlight("PRG", "TXL", 2, 30), d.get_flight_by_id(8))

        flights = d.get_flights("PRG", 0)
        self.assertEqual(len(flights), 3)
        self.assertEqual(flights[0], CFlight("PRG", "TXL", 0, 100))
        self.assertEqual(flights[1], CFlight("PRG", "BCN", 0, 50))
        self.assertEqual(flights[2], CFlight("PRG", "PRG", 0, 10))

        flights = d.get_flights("PRG", 0, cities_to_visit=["TXL", "BCN"])
        self.assertEqual(len(flights), 2)
        self.assertEqual(flights[0], CFlight("PRG", "TXL", 0, 100))
        self.assertEqual(flights[1], CFlight("PRG", "BCN", 0, 50))

        flights = d.get_flights("PRG", 0, cities_to_visit=["TXL", "BCN"],
                                sort_by_price=True)
        self.assertEqual(len(flights), 2)
        self.assertEqual(flights[0], CFlight("PRG", "BCN", 0, 50))
        self.assertEqual(flights[1], CFlight("PRG", "TXL", 0, 100))

        flights = d.get_flights_ids(0, 0)
        self.assertEqual(len(flights), 3)
        np.testing.assert_array_equal(flights[0], [0, 1, 0, 100])
        np.testing.assert_array_equal(flights[1], [0, 2, 0, 50])
        np.testing.assert_array_equal(flights[2], [0, 0, 0, 10])

        flights = d.get_flights_ids(0, 0, cities_to_visit_ids=[1,2])
        np.testing.assert_array_equal(len(flights), 2)
        np.testing.assert_array_equal(flights[0], [0, 1, 0, 100])
        np.testing.assert_array_equal(flights[1], [0, 2, 0, 50])

        flights = d.get_flights_ids(0, 0, cities_to_visit_ids=[1,2],
                                sort_by_price=True)
        np.testing.assert_array_equal(len(flights), 2)
        np.testing.assert_array_equal(flights[0], [0, 2, 0, 50])
        np.testing.assert_array_equal(flights[1], [0, 1, 0, 100])

    def test_num_flights(self):
        d = MatrixDataset()
        d.load_data('../input/3_airports_backtrace.csv')
        
        self.assertEqual( d.dataset.shape[0], 9 )

    def test_time(self):

        files = []
        files.append("../kiwisources/travelling-salesman/real_data/sorted_data/data_5.txt")
        files.append("../kiwisources/travelling-salesman/real_data/sorted_data/data_20.txt")
        files.append("../kiwisources/travelling-salesman/real_data/sorted_data/data_100.txt")
        files.append("../kiwisources/travelling-salesman/real_data/data_300.txt")

        def load(f):
            d = MatrixDataset()
            d.load_data(f)

        def time_and_tell(files, reps):
            for f in files:
                t = timeit(partial(load, f), number=reps)
                print("loading {} with MatrixDataset {} times: {}s".format(f, reps, t))

        # d = MatrixDataset()
        # d.load_data(files[0])
        # print( "{}\n^dataset".format( d.dataset ) )

        time_and_tell(files, 1)


if __name__ == '__main__':
    unittest.main()
