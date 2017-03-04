import unittest

import sys, os
sys.path.append(os.path.realpath(".."))

from src.searchers import BackTracker
from src.datasets import Flight

def load_data(path):
    # from src.datasets import DictDataset
    from src.datasets.CDictDataset import CDictDataset
    d = CDictDataset()
    # d.load_data('input/3_airports_input.csv')
    # d.load_data('../input/3_airports_backtrace.csv')
    d.load_data(path)
    return d

class BacktracerTest(unittest.TestCase):

    def test_backward(self):

        dataset = load_data('../input/3_airports_backtrace.csv')

        b = BackTracker()
        r = b.search(dataset)

        self.assertEqual(r[0], Flight("PRG", "TXL", 0, 100))
        self.assertEqual(r[1], Flight("TXL", "BCN", 1, 100))
        self.assertEqual(r[2], Flight("BCN", "PRG", 2, 100))

    def test_forward(self):

        dataset = load_data('../input/3_airports_input.csv')

        b = BackTracker()
        r = b.search(dataset)

        self.assertEqual(r[0], Flight("QSA", "EFQ", 0, 0))
        self.assertEqual(r[1], Flight("EFQ", "KCA", 1, 0))
        self.assertEqual(r[2], Flight("KCA", "QSA", 2, 0))

    def test_big(self):

        dataset = load_data('../input/300_90K_flights.csv')

        b = BackTracker()
        r = b.search(dataset)

        # self.assertEqual(r[0], Flight("QSA", "EFQ", 0, 0))
        # self.assertEqual(r[1], Flight("EFQ", "KCA", 1, 0))
        # self.assertEqual(r[2], Flight("KCA", "QSA", 2, 0))

if __name__ == '__main__':
    unittest.main()
