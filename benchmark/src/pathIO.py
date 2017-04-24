import sys,os
sys.path.append(os.path.realpath("../"))

from src.datasets import *

""" Little utility methods handling the "paths" files
    generated to keep track of results of performance
    testing of the methods """

def get_best_path(paths):
    if paths:
        return sorted(paths, key=lambda p: p.price)[0]
    else:
        return None

def parse_paths_file(file_name):

    if not os.path.exists(file_name):
        return None

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

def save_paths_file(paths, filename):

    paths = sorted(paths, key=lambda p: p.price)

    string = ''
    for i in range(len(paths)):
        p = paths[i]
        string += '{}\n'.format(p.price)
        for f in p.flights:
            string += '{} {} {} {}\n'.format(f.city_from, f.city_to,
                                             f.day, f.price)
        string = string[:-1]
        string += "\n\n" if i < (len(paths) -1) else ""
        with open(filename, 'w+') as f:
            f.write(string)
    return string
