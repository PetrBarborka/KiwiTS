import sys, os
import glob

sys.path.append(os.path.relpath('../'))

from src.generators.HenryGenerator2 import HenryGenerator2

""" A small script for generation of the benchmarking test files """

def clear_files(prefix=""):
    for f in glob.glob("{}*_input".format(prefix)) + \
             glob.glob("{}*_target".format(prefix)) + \
             glob.glob("{}*_all".format(prefix)):
        os.remove(os.path.realpath(f))

def gen_files(prefix=""):
    for num_airports in [5, 50, 100, 300]:

        total_flights = 10*num_airports
        # cheapest
        g = HenryGenerator2(num_airports=num_airports, flights_total=total_flights,
                            cheapest_path=True, paths_total=1) 

        g.save_input_file(path="{}{}_ap_{}_total_cheapest_input".format(prefix, num_airports, total_flights))
        g.save_target_file(path="{}{}_ap_{}_total_cheapest_target".format(prefix, num_airports, total_flights))
        g.save_all_paths_file(path="{}{}_ap_{}_total_cheapest_all".format(prefix, num_airports, total_flights))

        # most_expensive
        g = HenryGenerator2(num_airports=num_airports, flights_total=10*num_airports, 
                            most_expensive_path=True, paths_total=1) 

        g.save_input_file(path="{}{}_ap_{}_total_expensive_input".format(prefix, num_airports, total_flights))
        g.save_target_file(path="{}{}_ap_{}_total_expensive_target".format(prefix, num_airports, total_flights))
        g.save_all_paths_file(path="{}{}_ap_{}_total_expensive_all".format(prefix, num_airports, total_flights))

        # random
        g = HenryGenerator2(num_airports=num_airports, flights_total=10*num_airports, 
                            most_expensive_path=True, paths_total=5) 

        g.save_input_file(path="{}{}_ap_{}_total_random_input".format(prefix, num_airports, total_flights))
        g.save_target_file(path="{}{}_ap_{}_total_random_target".format(prefix, num_airports, total_flights))
        g.save_all_paths_file(path="{}{}_ap_{}_total_random_all".format(prefix, num_airports, total_flights))

prefix = "benchmarkdata/"
clear_files(prefix=prefix)
gen_files(prefix=prefix)
