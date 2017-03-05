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

    print('{:20}{}'.format('Iterations:', i))
    print('{:20}{}s'.format('Run time:', round(end - start, 5)))
    print('{:20}{}'.format('Cost:', sum(p.price for p in path)))
    print('{:20}{}'.format('Path:', path))
    print()

    return path


class RandomPathBuildingTest(unittest.TestCase):
    def test_run_basic(self):
        rpb = RandomPathBuilding()

        dataset = DictDataset()
        dataset.load_data('../input/3_airports_input.csv')

        path = run(rpb, dataset)
        self.assertEquals(len(path), 3)

        dataset = DictDataset()
        dataset.load_data('../input/3_airports_backtrace.csv')

        path = run(rpb, dataset)
        self.assertEquals(len(path), 3)

        dataset = DictDataset()
        dataset.load_data('../input/4_airports_backtrace.csv')

        path = run(rpb, dataset)
        self.assertEquals(len(path), 4)

    def test_run(self):
        dataset = DictDataset()
        dataset.load_data('../benchmark/benchmarkdata/data_100.txt')
        print('Data loaded.\n')

        rpb = RandomPathBuilding()
        # TODO: run async
        path = run(rpb, dataset)
        path = run(rpb, dataset)
        path = run(rpb, dataset)
        path = run(rpb, dataset)


if __name__ == '__main__':
    unittest.main()
