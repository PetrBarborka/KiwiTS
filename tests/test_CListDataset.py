import os
import sys
import unittest

sys.path.append(os.path.realpath(".."))

from src.datasets.CListDataset import CListDataset


class CListDatasetTest(unittest.TestCase):
    def test_cities(self):
        d = CListDataset()
        d.load_data('../input/3_airports_backtrace.csv')

        self.assertTrue("PRG" in d.cities)
        self.assertTrue("TXL" in d.cities)
        self.assertTrue("TXL" in d.cities)

    def test_num_flights(self):
        d = CListDataset()
        d.load_data('../input/3_airports_backtrace.csv')

        count = 0
        for city in d.dataset:
            for day in city:
                if day:
                    count += len(day)
        self.assertEquals(count, 9)


if __name__ == '__main__':
    unittest.main()
