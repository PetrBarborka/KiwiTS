import os
import sys
import unittest
import numpy as np

sys.path.append(os.path.realpath(".."))

from src.datasets import Flight
from src.searchers import Graph
from src.searchers import GraphACO

min_phe = 0.001
max_phe = 0.1


class GraphACOTest(unittest.TestCase):
    def test_run_basic(self):
        graph = Graph('../input/3_airports_input.csv', min_phe=min_phe, max_phe=max_phe)
        solver = GraphACO(graph.G, ants=5)
        path, cost = solver.search(10)

        self.assertEqual(cost, 0)
        # self.assertEquals(len(np.unique(path)), len(graph.G.nodes()))
        self.assertEqual(path[0], Flight("QSA", "EFQ", 0, 0))
        self.assertEqual(path[1], Flight("EFQ", "KCA", 1, 0))
        self.assertEqual(path[2], Flight("KCA", "QSA", 2, 0))

        graph = Graph('../input/3_airports_backtrace.csv', min_phe=min_phe, max_phe=max_phe)
        solver = GraphACO(graph.G, ants=5)
        path, cost = solver.search(10)

        self.assertEqual(cost, 300)
        # self.assertEquals(len(np.unique(path)), len(graph.G.nodes()))
        self.assertEqual(path[0], Flight("PRG", "TXL", 0, 100))
        self.assertEqual(path[1], Flight("TXL", "BCN", 1, 100))
        self.assertEqual(path[2], Flight("BCN", "PRG", 2, 100))

        graph = Graph('../input/4_airports_backtrace.csv', min_phe=min_phe, max_phe=max_phe)
        solver = GraphACO(graph.G, ants=5)
        path, cost = solver.search(10)

        self.assertEqual(cost, 400)
        # self.assertEquals(len(np.unique(path)), len(graph.G.nodes()))
        self.assertEqual(path[0], Flight("PRG", "TXL", 0, 100))
        self.assertEqual(path[1], Flight("TXL", "BCN", 1, 100))
        self.assertEqual(path[2], Flight("BCN", "DEL", 2, 100))
        self.assertEqual(path[3], Flight("DEL", "PRG", 3, 100))

    def test_run(self):
        graph = Graph('../input/50_airports_input.csv', min_phe=min_phe, max_phe=max_phe)
        solver = GraphACO(graph.G, ants=50, alpha=0.25, rho=0.25)
        path, cost = solver.search(500)

        # print ( cost )
        # for p in path:
            # print ( p )

        # self.assertEquals(len(np.unique(path)), len(graph.G.nodes()))


if __name__ == '__main__':
    unittest.main()
