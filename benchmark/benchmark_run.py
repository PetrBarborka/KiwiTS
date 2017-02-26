
import sys, os
import glob
from functools import partial

sys.path.append(os.path.relpath('../'))

from src.datasets import DictDataset
from src.searchers import BackTracker

import timeit

def initBackTracker(data_file):

    dataset = DictDataset()
    dataset.load_data(data_file)
    b = BackTracker()

    return dataset, b

def runBackTracker(dataset, b):

    b.search(dataset)

# def validateBackTracker(datafile, valid_paths_file, best_path_file):

def initIndians(data_file):

    dataset = DictDataset()
    dataset.load_data(data_file)
    t = Tribe()

    return dataset, t

def runIndians(dataset, t):

    t.search(dataset)

def initGraphBackTracker(data_file):

    return GraphBackTracker(Graph(data_file).G)

def runGraphBackTracker(solver):

    solver.search()

def initGraphACO(data_file):

    return GraphACO(Graph(data_file).G, ants=5)

def runGraphACO(solver):

    solver.search(10)

def benchmark_method(initfcn, runfcn, filename, reps):
    run_args = initBackTracker(file_name)
    t_init = timeit.timeit(partial(initBackTracker, file_name), number=reps)
    t_run = timeit.timeit(partial(runBackTracker, *run_args), number=reps)

    return t_init, t_run

reps = 100
file_name = "benchmarkdata/300_ap_3000_total_random_input"

t_init, t_run = benchmark_method(initBackTracker, runBackTracker, file_name, reps)

print("Backtracker load time: {}".format(t_init/reps))
print("Backtracker run time: {}".format(t_run/reps))

t_init, t_run = benchmark_method(initIndians, runIndians, file_name, reps)

print("Indians load time: {}".format(t_init/reps))
print("Indians run time: {}".format(t_run/reps))

t_init, t_run = benchmark_method(initGraphBackTracker, runGraphBackTracker, file_name, reps)

print("GraphBackTracker load time: {}".format(t_init/reps))
print("GraphBackTracker run time: {}".format(t_run/reps))

t_init, t_run = benchmark_method(initGraphACO, runGraphACO, file_name, reps)

print("GraphACO load time: {}".format(t_init/reps))
print("GraphACO run time: {}".format(t_run/reps))
