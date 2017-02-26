from operator import itemgetter
from heapq import heappush, heappop

from src.datasets import Flight


class GraphShortestPath:
    def __init__(self, G):
        self.G = G
        self.start_city = G.graph['start_city']

    def _shortest_path(self):
        dists = {}
        paths = {(self.start_city, 0): []}
        seen = {(self.start_city, 0): 0}
        fringe = []

        heappush(fringe, (0, 0, self.start_city))

        while fringe:
            (price, today, city_from) = heappop(fringe)

            if (city_from, today) in dists:
                continue
            else:
                dists[(city_from, today)] = price

            # connections to start city MUST be on last day only
            if city_from == self.start_city and today != 0:
                break

            flights = []
            for city_to, flight_data in self.G[city_from].items():
                possible_flights = [(data['weight'], data['day']) for _, data in flight_data.items() if
                                    data['day'] == today]

                if possible_flights:
                    best_flight = min(possible_flights, key=itemgetter(0))
                    flights.append((city_to, {'weight': best_flight[0], 'day': best_flight[1]}))

            for city_to, flight_data in flights:
                dist = dists[(city_from, flight_data['day'])] + flight_data['weight']
                tomorrow = today + 1

                if (city_to, tomorrow) not in seen or dist < seen[(city_to, tomorrow)]:
                    seen[(city_to, tomorrow)] = dist
                    paths[(city_to, tomorrow)] = paths[(city_from, today)] + [
                        Flight(city_from, city_to, today, flight_data['weight'])]
                    heappush(fringe, (dist, tomorrow, city_to))

        return paths, dists

    def search(self):
        last_day = len(self.G.nodes())
        paths, dists = self._shortest_path()
        return paths[(self.start_city, last_day)], dists[(self.start_city, last_day)]
