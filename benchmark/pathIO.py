import sys,os
sys.path.append(os.path.realpath("../"))

from src.datasets import *

def parse_target_file(file_name):
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

file_name = "benchmarkdata/5_ap_50_total_random_all"
print ( parse_target_file(file_name) )
