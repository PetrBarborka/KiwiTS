import sys
import fileinput
from collections import namedtuple

Flight = namedtuple('Flight', 'FROM TO DOD PRICE')

def read_file(filename=None):
    flights = []
    for i, line in enumerate(fileinput.input(filename)):
        if i != 0:
            flights.append(process_line(line))
        else:
            start = line.rstrip()
    return start, flights


def process_line(line):
    lst = line.rstrip().split(' ')
    return Flight(lst[0], lst[1], int(lst[2]), int(lst[3]))
