from DatasetInterface import DatasetInterface

import sys


class DictDataset(DatasetInterface):
    def __init__(self):
        self.dataset = dict()

    def load_data(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()
    def get_flights(self, airport_code, day):
        pass

d = DictDataset()
d.load_data(sys.argv[1])
