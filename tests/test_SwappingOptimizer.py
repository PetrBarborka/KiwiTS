import os
import sys
import unittest

sys.path.append(os.path.realpath(".."))

from src.datasets import Flight
from src.datasets import DictDataset
from src.searchers import BackTracker
from src.optimalization import SwappingOptimizer


class ShortestPathTest(unittest.TestCase):
    def test_run(self):
        dataset = DictDataset()
        dataset.load_data('../input/3_airports_input.csv')


if __name__ == '__main__':
    unittest.main()
