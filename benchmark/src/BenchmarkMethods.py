import sys, os

sys.path.append(os.path.relpath('../../'))

from BenchmarkMethodInterface import *
from src.datasets import *
from src.datasets.CDictDataset import CDictDataset
from src.searchers import *

from multiprocessing import Process

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

class BenchmarkBackTracker_Cython(BenchmarkMethodInterface):

    def __init__(self):
        super().__init__()
        self.dataset = None
        self.backtracker = None

    def initialize(self, data_file):
        dataset = CDictDataset()
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

        flights = self.tribe.search(self.dataset)
        totalcost = sum([f.price for f in flights])
        self.result = DataPath(flights, totalcost)

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

class BenchmarkRandomPathBuilding(BenchmarkMethodInterface):

    def __init__(self):
        super().__init__()
        self.dataset = None
        self.rpb = None

    def initialize(self, data_file):
        dataset = CDictDataset()
        dataset.load_data(data_file)

        self.dataset = dataset
        self.rpb = RandomPathBuilding()

    def run(self):
        
        assert self.dataset and self.rpb, "initialize before running"
        flights = self.rpb.search(self.dataset)
        if flights: 
            totalcost = sum([f.price for f in flights])
            self.result = DataPath(flights, totalcost)

if __name__ == "__main__":
    
    # input_file = "../benchmarkdata/5_ap_50_total_random_input"
    # valid_results_file = "../benchmarkdata/5_ap_50_total_random_all"

    # input_file = "../benchmarkdata/300_ap_3000_total_random_input"
    # valid_results_file = "../benchmarkdata/300_ap_3000_total_random_all"
    #
    # input_file = "../../input/500_airports_input.csv"
    # valid_results_file = "paths.csv"
    #

    # input_file = "../../kiwisources/travelling-salesman/real_data/sorted_data/data_200.txt"
    input_file = "../../kiwisources/travelling-salesman/real_data/data_300.txt"
    valid_results_file = "paths.csv"

    timeout = 200
    # timeout = 10

    for b in [BenchmarkBackTracker(),  BenchmarkBackTracker_Cython(), BenchmarkIndians(), 
              BenchmarkGraphBackTracker(), BenchmarkACO(), BenchmarkShortestPath(),
              BenchmarkRandomPathBuilding()]:

        print( "--- {} ---".format(b.__class__.__name__))
        p = Process(target=partial(b.benchmark, input_file, valid_results_file=valid_results_file, reps=1, timeout=timeout))
        p.start()
        p.join(timeout=timeout)
        if p.is_alive():
            p.terminate()
            print("timeout of {} seconds exceeded for".format(timeout))
            continue


