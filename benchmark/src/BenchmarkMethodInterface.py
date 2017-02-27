import sys, os

sys.path.append(os.path.relpath('../../'))

from src.datasets import *

class BenchmarkMethodInterface:
    """Set whatever you want in __init__, but leave any real data manipulation
       to initialize(). Set self.result to a DataPath in run() for validation.
       Assert initialization in run """

    def __init__(self):
        self.result = None
        self.result_valid = None
        self.result_optimal = None

    def initialize(self, data_path):
        """ Load data """
        raise NotImplementedError( "Should have implemented this" )

    def run(self):
        raise NotImplementedError( "Should have implemented this" )

    def validate(self, valid_paths_file, best_path_file):
        
        assert self.dataset and self.backtracker and self.result, \
                "initialize, run and then validate"

        valid_paths = self._parse_target_file(valid_paths_file)
        optimal_path = self._parse_target_file(best_path_file)[0]

        self.result_valid = self.result in valid_paths
        self.result_optimal = self.result == optimal_path

        #what if we found a path that we didn't put in?
        if not self.result_valid and self.result.is_valid():
            self.result_valid = True
            if self.result.price <= optimal_path.price:
                self.result_optimal = True

        return self.result_valid

    def _parse_target_file(self, file_name):

        with open(file_name) as f:
            lines = []
            paths = []
            path = []
            cost = 0
            for line in f:
                line = line.replace("\n", "")
                line = line.split(" ")
                if line[0] == "":
                    continue
                lines.append(line)
                if len(line) == 1:
                    if path:
                        paths.append(DataPath(path, cost))
                    path = []
                    cost = int(line[0])
                    continue
                path.append(Flight(*line))
            if path:
                paths.append(DataPath(path,cost))

        return paths
