import networkx as nx

from copy import deepcopy
from src.datasets import Flight


class GraphBackTracker:
    def __init__(self, start_city, flights):
        self.start_city = start_city
        self.to_visit = {flt.city_from for flt in flights}
        self.last_day = len(self.to_visit) - 1
        self.G = self._build_graph(flights)

    def _build_graph(self, flights):
        """
        Build directed graph with multiple edges between nodes.
        :param flights: list with flights
        :return: networkx graph
        """
        graph = nx.MultiDiGraph()

        for flt in flights:
            if self._is_new_edge(flt):
                graph.add_edge(flt.city_from, flt.city_to, weight=flt.price, day=flt.day)

        return graph

    def _is_new_edge(self, flight):
        """
        Check whether to create new edge or not to limit redundant edges.
        :param flight: flight object
        :return: boolean value
        """
        # allow only flights from the starting city on first day of the trip
        is_first_day_flight = flight.city_from == self.start_city and flight.day == 0
        # allow only flights to the starting city on the last day of the trip
        is_last_day_flight = flight.city_to == self.start_city and flight.day == self.last_day
        # do not allow flights to the starting city during the trip
        is_midtrip_flight = flight.day != 0 and flight.day != self.last_day and self.start_city not in [
            flight.city_from,
            flight.city_to]
        # do not allow flights from and back to the same city
        is_same_city = flight.city_from == flight.city_to

        return (is_first_day_flight or is_last_day_flight or is_midtrip_flight) and not is_same_city

    def backtracking(self):
        """
        Nearest neighbor backtracking.
        :return: cost, list with taken flights
        """
        to_visit = list(deepcopy(self.to_visit))

        cost = 0
        path = []
        tabu = {}
        current_day = 0
        current_city = self.start_city

        while to_visit:
            # select all edges/flights to unvisited cities from current city on current day
            possible_flights = [(city_from, city_to, data) for (city_from, city_to, data) in
                                self.G.edges(current_city, data=True)
                                if data['day'] == current_day and city_to in to_visit and not tabu.get(
                        (city_from, city_to, data['day'], data['weight']), False)]

            if possible_flights:
                # weight == prize
                best_flight = min(possible_flights, key=lambda (u, v, d): d['weight'])

                cost += best_flight[2]['weight']
                current_city = best_flight[1]
                current_day += 1

                to_visit.remove(current_city)
                path.append(Flight(best_flight[0], best_flight[1], best_flight[2]['day'], best_flight[2]['weight']))
            else:
                # remove last flight from path
                last_flight = path.pop(-1)
                to_visit.append(current_city)

                cost -= last_flight.price
                current_city = last_flight.city_from
                current_day -= 1

                tabu[(last_flight.city_from, last_flight.city_to, last_flight.day, last_flight.price)] = 1

        return cost, path

    def indians(self):
        # TODO: implement some simple benchmark
        pass

    def search(self, mode='backtracking'):
        if mode == 'backtracking':
            return self.backtracking()
        elif mode == 'indians':
            # self.indians()
            raise NotImplementedError('TODO')
        else:
            raise NotImplementedError()
