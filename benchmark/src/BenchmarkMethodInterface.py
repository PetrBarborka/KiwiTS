import sys, os

sys.path.append(os.path.relpath('../../'))

from src.datasets import *
from pathIO import *

import timeit, time

from functools import partial

class BenchmarkMethodInterface:
    """Set whatever you want in __init__, but leave any real data manipulation
       to initialize(). Set self.result to a DataPath in run() for validation.
       Assert initialization in run """

    def __init__(self):
        self.result = None
        self.result_is_valid = None
        self.result_is_best_known = None

    def initialize(self, data_path):
        """ Load data """
        raise NotImplementedError( "Should have implemented this" )

    def run(self):
        raise NotImplementedError( "Should have implemented this" )

    def validate(self, known_paths_file=None):
        
        assert self.result, "initialize, run and then validate"

        known_paths = parse_paths_file(known_paths_file)

        if known_paths is not None:
            best_known_path = get_best_path(known_paths)
            self.result_is_valid = self.result in known_paths
            self.result_is_best_known = self.result == best_known_path
        else:
            known_paths = []
            best_known_path = None

        #what if we found a path that we didn't put in?
        if not self.result_is_valid and self.result.is_valid():
            self.result_is_valid = True

            if best_known_path and self.result.price <= best_known_path.price:
                print( "New best path discovered!" )
                self.result_is_best_known = True


            known_paths.append(self.result)
            save_paths_file(known_paths, known_paths_file)

        return self.result_is_valid

    def benchmark(self, input_file, valid_results_file=None, reps=10, timeout=10):

        t_init = timeit.timeit(partial(self.initialize, input_file), number=reps)/reps
        t_run = timeit.timeit(self.run, number=reps)/reps

        print( "input: {}, {} reps".format(input_file, reps) )
        print( "average time: {:.6f} ({:.6f} + {:.6f})".format(t_init + t_run, t_init, t_run))

        if self.result :
            if len( self.result.flights ) > 10:
                print( "->path: {} ... {} \n->price: {}".format(self.result.flights[:3], 
                                                             self.result.flights[-3:],
                                                             self.result.price) )
            else:
                print( "->path: {}\n ->price: {}".format(self.result.flights, self.result.price) )

            self.validate(valid_results_file)
            print ( "Result valid?: {}".format(self.result_is_valid) )
            print ( "Result best known?: {}".format(self.result_is_best_known) )

        else:
            print ( "Failed to find path" )

