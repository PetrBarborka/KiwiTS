import os
import sys
import unittest
import numpy as np

sys.path.append(os.path.realpath(".."))

from src.datasets import Flight
from src.searchers import Graph
from src.searchers import GraphShortestPath


class GraphShortestPathTest(unittest.TestCase):
    def test_run_basic(self):
        graph = Graph('../input/3_airports_input.csv')
        solver = GraphShortestPath(graph.G)
        path, cost = solver.search()

        self.assertEquals(cost, 0)
        self.assertEquals(len(np.unique(path)), len(graph.G.nodes()))
        self.assertEqual(path[0], Flight("QSA", "EFQ", 0, 0))
        self.assertEqual(path[1], Flight("EFQ", "KCA", 1, 0))
        self.assertEqual(path[2], Flight("KCA", "QSA", 2, 0))

        graph = Graph('../input/3_airports_backtrace.csv')
        solver = GraphShortestPath(graph.G)
        path, cost = solver.search()

        self.assertEquals(cost, 300)
        self.assertEquals(len(np.unique(path)), len(graph.G.nodes()))
        self.assertEqual(path[0], Flight("PRG", "TXL", 0, 100))
        self.assertEqual(path[1], Flight("TXL", "BCN", 1, 100))
        self.assertEqual(path[2], Flight("BCN", "PRG", 2, 100))

        graph = Graph('../input/4_airports_backtrace.csv')
        solver = GraphShortestPath(graph.G)
        path, cost = solver.search()

        self.assertEquals(cost, 400)
        self.assertEquals(len(np.unique(path)), len(graph.G.nodes()))
        self.assertEqual(path[0], Flight("PRG", "TXL", 0, 100))
        self.assertEqual(path[1], Flight("TXL", "BCN", 1, 100))
        self.assertEqual(path[2], Flight("BCN", "DEL", 2, 100))
        self.assertEqual(path[3], Flight("DEL", "PRG", 3, 100))

    def test_run(self):
        graph = Graph('../input/300_airports_input.csv')
        solver = GraphShortestPath(graph.G)
        path, cost = solver.search()

        self.assertEquals(len(np.unique(path)), len(graph.G.nodes()))
        print cost
        for p in path:
            print p


if __name__ == '__main__':
    unittest.main()
