import unittest

import sys, os
sys.path.append(os.path.realpath(".."))

from timeit import timeit
from functools import partial

from subprocess import call

import numpy as np

from src.datasets import CMatrixDataset
from src.datasets import CDictDataset
from src.datasets import CListDataset
from src.datasets import DictDataset
from src.datasets import CFlight

class DatasetComparisonTest(unittest.TestCase):

    def test_time(self):

        repo = "../kiwisources/travelling-salesman/"
        files = []
        files.append("{}real_data/sorted_data/data_5.txt".format(repo))
        files.append("{}real_data/sorted_data/data_20.txt".format(repo))
        # files.append("{}real_data/sorted_data/data_100.txt".format(repo))
        # files.append("{}real_data/data_300.txt".format(repo))

        def load(input_file, dataset_class, stdin=False):
            if stdin:
                dataset_class().load_data(stdin=True)
            else:
                dataset_class().load_data(input_file)

        def time_and_tell(classes, files, reps):
            for f in files:
                print("loading {} {} times:".format(f,reps))
                for c in classes:
                    t = timeit(partial(load, f, c), number=reps)
                    print("\t{} \t: {}s".format(c.__name__, t))

        def time_stdin(classes, files, reps):
            for f in files:
                print("loading {} from STDIN {} times:".format(f,reps))
                for c in classes:
                    p = partial(call, "cat {} | python3 helper_load_CDictDataset_stdin.py".format(f), shell=True)
                    t = timeit(p, number=reps)
                    print("\t{} \t: {}s".format(c.__name__, t))


        # classes = [CMatrixDataset, CDictDataset, CListDataset, DictDataset]
        # classes = [CMatrixDataset, CDictDataset, CListDataset]
        classes = [CDictDataset]
        time_and_tell(classes, files, 1)
        time_stdin(classes, files, 1)


if __name__ == '__main__':
    unittest.main()
