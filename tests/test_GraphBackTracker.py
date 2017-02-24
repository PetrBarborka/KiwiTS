import os
import sys
import unittest
import fileinput

sys.path.append(os.path.realpath(".."))

from src.datasets import Flight
from src.searchers import GraphBackTracker


def load_data(filename=None):
    """
    Read flights from file or STDIN.
    :param filename: optional, else reads from STDIN
    :return: starting city, list with flights
    """
    flights = []

    for i, line in enumerate(fileinput.input(filename)):
        if i != 0:
            flights.append(process_line(line))
        else:
            start = line.rstrip()

    return start, flights


def process_line(line):
    """
    Process one flight.
    :param line: string in format 'FROM TO DOD PRICE'
    :return: Flight object
    """
    lst = line.rstrip().split(' ')
    return Flight(lst[0], lst[1], int(lst[2]), int(lst[3]))


class GraphBackTrackerTest(unittest.TestCase):
    def test_forward(self):
        start_city, flights = load_data('../input/3_airports_input.csv')

        solver = GraphBackTracker(start_city, flights)
        cost, path = solver.search()

        self.assertEquals(cost, 0)

        self.assertEqual(path[0], Flight("QSA", "EFQ", 0, 0))
        self.assertEqual(path[1], Flight("EFQ", "KCA", 1, 0))
        self.assertEqual(path[2], Flight("KCA", "QSA", 2, 0))

    def test_backward(self):
        start_city, flights = load_data('../input/3_airports_backtrace.csv')

        solver = GraphBackTracker(start_city, flights)
        cost, path = solver.search()

        self.assertEquals(cost, 300)
        self.assertEqual(path[0], Flight("PRG", "TXL", 0, 100))
        self.assertEqual(path[1], Flight("TXL", "BCN", 1, 100))
        self.assertEqual(path[2], Flight("BCN", "PRG", 2, 100))

        start_city, flights = load_data('../input/4_airports_backtrace.csv')

        solver = GraphBackTracker(start_city, flights)
        cost, path = solver.search()

        self.assertEquals(cost, 400)
        self.assertEqual(path[0], Flight("PRG", "TXL", 0, 100))
        self.assertEqual(path[1], Flight("TXL", "BCN", 1, 100))
        self.assertEqual(path[2], Flight("BCN", "DEL", 2, 100))
        self.assertEqual(path[3], Flight("DEL", "PRG", 3, 100))


if __name__ == '__main__':
    unittest.main()
