import unittest

import sys, os
sys.path.append(os.path.realpath(".."))

from src.searchers import BackTracker
from src.datasets import Flight

def load_data(path):
    from src.datasets import DictDataset
    d = DictDataset()
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


    # def test_cities(self):
    #     from src.datasets import DictDataset
    #     d = DictDataset()
    #     d.load_data('../input/3_airports_backtrace.csv')
    #
    #     self.assertTrue("PRG" in d.cities )
    #     self.assertTrue("TXL" in d.cities )
    #     self.assertTrue("TXL" in d.cities )
    #
    # def test_num_flights(self):
    #     from src.datasets import DictDataset
    #     d = DictDataset()
    #     d.load_data('../input/3_airports_backtrace.csv')
    #
    #     count = 0
    #     for ap in d.dataset:
    #         for day in d.dataset[ap]:
    #             for flight in d.dataset[ap][day]:
    #                 count += 1
    #     self.assertEquals( count, 9 )

if __name__ == '__main__':
    unittest.main()
