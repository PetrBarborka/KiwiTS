import unittest

import sys, os
sys.path.append(os.path.realpath(".."))

from timeit import timeit
from functools import partial

import numpy as np

from src.datasets import CMatrixDataset
from src.datasets import CDictDataset
from src.datasets import CListDataset
from src.datasets import DictDataset
from src.datasets import CFlight

class DatasetComparisonTest(unittest.TestCase):

    def test_time(self):

        files = []
        files.append("../kiwisources/travelling-salesman/real_data/sorted_data/data_5.txt")
        files.append("../kiwisources/travelling-salesman/real_data/sorted_data/data_20.txt")
        files.append("../kiwisources/travelling-salesman/real_data/sorted_data/data_100.txt")
        files.append("../kiwisources/travelling-salesman/real_data/data_300.txt")

        def load(input_file, dataset_class):
            dataset_class().load_data(input_file)

        def time_and_tell(classes, files, reps):
            for f in files:
                print("loading {} {} times:".format(f,reps))
                for c in classes:
                    t = timeit(partial(load, f, c), number=reps)
                    print("\t{} \t: {}s".format(c.__name__, t))

        classes = [CMatrixDataset, CDictDataset, CListDataset, DictDataset]
        time_and_tell(classes, files, 1)


if __name__ == '__main__':
    unittest.main()
