import sys, os

sys.path.append(os.path.relpath('../../'))

from BenchmarkMethodInterface import *
from src.datasets import *
from src.searchers import *

class BenchmarkBackTracker(BenchmarkMethodInterface):

    def __init__(self):
        self.dataset = None
        self.backtracker = None
        self.result = None
        self.result_valid = None
        self.result_optimal = None

    def initialize(self, data_file):
        dataset = DictDataset()
        dataset.load_data(data_file)

        self.dataset = dataset
        self.backtracker = BackTracker()

    def run(self):
        
        assert self.dataset and self.backtracker, "initialize before running"
        flights = self.backtracker.search(self.dataset)
        totalcost = sum([f.price for f in flights])
        self.result = DataPath(flights, totalcost)


if __name__ == "__main__":
    
    input_file = "../benchmarkdata/5_ap_50_total_random_input"
    valid_results_file = "../benchmarkdata/5_ap_50_total_random_all"
    target_file = "../benchmarkdata/5_ap_50_total_random_target"
    
    b = BenchmarkBackTracker()
    b.initialize(input_file)
    b.run()
    print( repr(b.result) )
    b.validate(valid_results_file, target_file)
    print ( "Result valid?: {}".format(b.result_valid) )
    print ( "Result optimal?: {}".format(b.result_optimal) )

