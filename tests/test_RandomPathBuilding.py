import os
import sys
import unittest

sys.path.append(os.path.realpath(".."))

from timeit import default_timer as timer

from src.datasets import DictDataset
from src.searchers import RandomPathBuilding


def run(rpb, dataset):
    i = 0
    path = None

    start = timer()
    while not path:
        i += 1
        path = rpb.search(dataset)
    end = timer()

    return i, path, end-start


class RandomPathBuildingTest(unittest.TestCase):
    def test_run_basic(self):
        rpb = RandomPathBuilding()

        dataset = DictDataset()
        dataset.load_data('../input/3_airports_input.csv')

        path = run(rpb, dataset)[1]
        self.assertEquals(len(path), 3)

        dataset = DictDataset()
        dataset.load_data('../input/3_airports_backtrace.csv')

        path = run(rpb, dataset)[1]
        self.assertEquals(len(path), 3)

        dataset = DictDataset()
        dataset.load_data('../input/4_airports_backtrace.csv')

        path = run(rpb, dataset)[1]
        self.assertEquals(len(path), 4)

    def test_run(self):
        dataset = DictDataset()
        dataset.load_data('../benchmark/benchmarkdata/data_100.txt')
        print('Data loaded.\n')

        rpb = RandomPathBuilding()

        path = []
        cost = sys.maxsize
        iters = 0
        time_taken = 0

        start = timer()
        for i in range(1000):
            new_iters, new_path, new_time_taken = run(rpb, dataset)
            new_cost = sum(p.price for p in new_path)
            if new_cost < cost:
                cost = new_cost
                path = new_path
                iters = new_iters
                time_taken = new_time_taken
        end = timer()

        print('{:20}{}'.format('Iterations:', iters))
        print('{:20}{}s'.format('Run time:', round(time_taken, 5)))
        print('{:20}{}'.format('Cost:', cost))
        print('{:20}{}'.format('Path:', path))
        print('\nFinished in {}s'.format(round(end - start, 5)))


if __name__ == '__main__':
    unittest.main()
