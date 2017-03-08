import os
import sys
import unittest

sys.path.append(os.path.realpath(".."))

from timeit import default_timer as timer

from src.datasets import CDictDataset
from src.searchers import BackTracker
from src.optimalization import SwappingOptimizer


class SwappingOptimizerTest(unittest.TestCase):
    def test_run_simple(self):
        dataset = CDictDataset()
        dataset.load_data('../input/5_airports_optimizer.csv')

        so = SwappingOptimizer()

        path = [dataset.get_flight_by_id(i) for i in range(5)]
        optimized_path = so.run(path[:], dataset)

        cost = sum([p.price for p in path])
        optimized_cost = sum([p.price for p in optimized_path])
        self.assertLess(optimized_cost, cost)

        print(cost, path)
        print(optimized_cost, optimized_path)

    def test_run(self):
        dataset = CDictDataset()
        dataset.load_data('../input/data_200.txt')

        so = SwappingOptimizer()
        b = BackTracker()

        path = b.search(dataset)
        optimized_path = so.run(path[:], dataset, 10)

        cost = sum([p.price for p in path])
        start = timer()
        optimized_cost = sum([p.price for p in optimized_path])
        end = timer()

        all_from = [p.city_from for p in optimized_path]
        all_to = [p.city_to for p in optimized_path]
        self.assertEquals(len(all_from), len(set(all_from)))
        self.assertEquals(len(all_to), len(set(all_to)))

        print('{:20}{}s'.format('Run time:', round(end - start, 5)))
        print(cost, path)
        print(optimized_cost, optimized_path)


if __name__ == '__main__':
    unittest.main()
