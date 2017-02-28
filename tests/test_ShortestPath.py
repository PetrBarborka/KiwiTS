import os
import sys
import unittest

sys.path.append(os.path.realpath(".."))

from src.datasets import Flight
from src.datasets import DictDataset
from src.searchers import ShortestPath
from src.searchers import Tribe


class ShortestPathTest(unittest.TestCase):
    def test_run_basic(self):
        sp = ShortestPath()

        dataset = DictDataset()
        dataset.load_data('../input/3_airports_input.csv')

        path, price = sp.search(dataset)

        self.assertEquals(price, 0)
        self.assertEquals(len(path), 3)
        self.assertEqual(path[0], Flight("QSA", "EFQ", 0, 0))
        self.assertEqual(path[1], Flight("EFQ", "KCA", 1, 0))
        self.assertEqual(path[2], Flight("KCA", "QSA", 2, 0))

        dataset = DictDataset()
        dataset.load_data('../input/3_airports_backtrace.csv')

        path, price = sp.search(dataset)

        self.assertEquals(price, 300)
        self.assertEquals(len(path), 3)
        self.assertEqual(path[0], Flight("PRG", "TXL", 0, 100))
        self.assertEqual(path[1], Flight("TXL", "BCN", 1, 100))
        self.assertEqual(path[2], Flight("BCN", "PRG", 2, 100))

        dataset = DictDataset()
        dataset.load_data('../input/4_airports_backtrace.csv')

        path, price = sp.search(dataset)

        self.assertEquals(price, 400)
        self.assertEquals(len(path), 4)
        self.assertEqual(path[0], Flight("PRG", "TXL", 0, 100))
        self.assertEqual(path[1], Flight("TXL", "BCN", 1, 100))
        self.assertEqual(path[2], Flight("BCN", "DEL", 2, 100))
        self.assertEqual(path[3], Flight("DEL", "PRG", 3, 100))

    def test_run(self):
        dataset = DictDataset()
        dataset.load_data('../benchmark/benchmarkdata/300_ap_3000_total_random_input')

        sp = ShortestPath()
        path, price = sp.search(dataset)

        print(price)
        for p in path:
            print(p)


if __name__ == '__main__':
    unittest.main()
