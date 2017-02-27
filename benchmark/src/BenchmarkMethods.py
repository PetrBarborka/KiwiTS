import sys, os

sys.path.append(os.path.relpath('../../'))

from BenchmarkMethodInterface import *
from src.datasets import *
from src.searchers import *

class BenchmarkBackTracker(BenchmarkMethodInterface):

    def __init__(self):
        super().__init__()
        self.dataset = None
        self.backtracker = None

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

class BenchmarkIndians(BenchmarkMethodInterface):

    def __init__(self):
        super().__init__()
        self.dataset = None
        self.tribe = None

    def initialize(self, data_file):
        dataset = DictDataset()
        dataset.load_data(data_file)

        self.dataset = dataset
        self.tribe = Tribe()

    def run(self):

        assert self.dataset and self.tribe, "initialize before running"
        r = self.tribe.search(self.dataset)
        flights = [self.dataset.get_flight_by_id(f) for f in r.flights]
        self.result = DataPath(flights, r.price)

class BenchmarkGraphBackTracker(BenchmarkMethodInterface):

    def __init__(self):
        super().__init__()
        self.gbt = None

    def initialize(self, data_file):

        self.gbt = GraphBackTracker(Graph(data_file).G)

    def run(self):

        assert self.gbt, "initialize before running"
        r = self.gbt.search()
        # flights = [self.dataset.get_flight_by_id(f) for f in r.flights]
        self.result = DataPath(r[1], r[0])

class BenchmarkACO(BenchmarkMethodInterface):

    def __init__(self):
        super().__init__()
        self.gAnt = None

    def initialize(self, data_file):

        self.gAnt = GraphACO(Graph(data_file).G, ants=5)

    def run(self):

        assert self.gAnt, "initialize before running"
        r = self.gAnt.search(10)
        self.result = DataPath(r[0], r[1])

class BenchmarkShortestPath(BenchmarkMethodInterface):

    def __init__(self):
        super().__init__()
        self.gSP = None

    def initialize(self, data_file):

        self.gSP = GraphShortestPath(Graph(data_file).G)

    def run(self):

        assert self.gSP, "initialize before running"
        r = self.gSP.search()
        # flights = [self.dataset.get_flight_by_id(f) for f in r.flights]
        self.result = DataPath(r[0], r[1])

if __name__ == "__main__":
    
    # input_file = "../benchmarkdata/5_ap_50_total_random_input"
    # valid_results_file = "../benchmarkdata/5_ap_50_total_random_all"

    # input_file = "../benchmarkdata/300_ap_3000_total_random_input"
    # valid_results_file = "../benchmarkdata/300_ap_3000_total_random_all"
    #
    # input_file = "../../input/500_airports_input.csv"
    # valid_results_file = "paths.csv"
    #

    input_file = "../../kiwisources/travelling-salesman/real_data/sorted_data/data_200.txt"
    valid_results_file = "paths.csv"


    # for bclass in [BenchmarkBackTracker, BenchmarkIndians, BenchmarkGraphBackTracker,
    #                BenchmarkACO, BenchmarkShortestPath]:

    timeout = 30

    for bclass in [BenchmarkBackTracker, BenchmarkIndians, BenchmarkGraphBackTracker,
                   BenchmarkACO, BenchmarkShortestPath]:

        def timed_run():
            print( "--- {} ---".format(bclass.__name__))
            b = bclass()
            b.initialize(input_file)
            b.run()
            print( repr(b.result) )
            print( b.result.price )
            b.validate(valid_results_file)
            print ( "Result valid?: {}".format(b.result_is_valid) )
            print ( "Result best known?: {}".format(b.result_is_best_known) )

        p = Process(target=timed_run)
        p.start()

        p.join(timeout=timeout)

        if p.is_alive():
            p.terminate()
            print("Initial run: timeout of {} seconds exceeded".format(timeout))

        b = bclass()
        b.benchmark(input_file, reps=1, timeout=timeout)

