import fileinput
import networkx as nx

from src.datasets import Flight


class Graph:
    def __init__(self, path):
        self.G = self._build_graph(path)

    def _load_data(self, path=None):
        flights = []
        for i, line in enumerate(fileinput.input(path)):
            if i != 0:
                flights.append(self._process_line(line))
            else:
                start = line.rstrip()
        return start, flights

    def _process_line(self, line):
        lst = line.rstrip().split(' ')
        return Flight(lst[0], lst[1], int(lst[2]), int(lst[3]))

    def _is_new_edge(self, flight, start_city, last_day):
        # allow only flights from the starting city on first day of the trip
        is_first_day_flight = flight.city_from == start_city and flight.day == 0
        # allow only flights to the starting city on the last day of the trip
        is_last_day_flight = flight.city_to == start_city and flight.day == last_day
        # do not allow flights to the starting city during the trip
        is_midtrip_flight = flight.day != 0 and flight.day != last_day and start_city not in [
            flight.city_from,
            flight.city_to]
        # do not allow flights from and back to the same city
        is_same_city = flight.city_from == flight.city_to

        return (is_first_day_flight or is_last_day_flight or is_midtrip_flight) and not is_same_city

    def _build_graph(self, path):
        start_city, flights = self._load_data(path)
        to_visit = {flt.city_from for flt in flights}
        last_day = len(to_visit) - 1

        graph = nx.MultiDiGraph(start_city=start_city)

        for flt in flights:
            if self._is_new_edge(flt, start_city, last_day):
                graph.add_edge(flt.city_from, flt.city_to, weight=flt.price, day=flt.day)

        return graph
