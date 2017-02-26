import sys
import random

from src.datasets import Flight


class GraphACO:
    def __init__(self, G, ants=2, alpha=1, beta=1, mu=100, rho=0.5, min_phe=0.001, max_phe=0.1, phe_reinit=50,
                 evaporation=True):
        self.G = G
        self.start_city = G.graph['start_city']
        self.ants = ants
        self.alpha = alpha
        self.beta = beta
        self.mu = mu
        self.rho = rho
        self.min_phe = min_phe
        self.max_phe = max_phe
        self.phe_reinit = phe_reinit
        self.evaporation = evaporation

    def _calculate_neighbours_probabilities(self, neighbours):
        # total pheromone neighbourhood
        min_val = 0.00001
        neighbours_phe = 0
        for n in neighbours:
            neighbours_phe += n[2]['phe'] ** self.alpha * (1.0 / max(n[2]['weight'], min_val)) ** self.beta

        # probability per neighbour
        for n in neighbours:
            prob = (n[2]['phe'] ** self.alpha * (1.0 / max(n[2]['weight'], min_val)) ** self.beta) / neighbours_phe
            yield n[1], prob, n[2]['weight']

    def _select_neighbour(self, neighbours):
        bottom = 0
        rand = random.random()

        for city_to, prob, price in self._calculate_neighbours_probabilities(neighbours):
            if bottom < rand <= bottom + prob:
                return city_to, price
            bottom += prob

    def _construct_paths(self):
        paths = []
        days_and_prices = []
        max_days = self.G.order() - 1

        for ant in range(self.ants):
            to_visit = self.G.nodes()
            current_city = self.start_city
            current_day = 0

            path = [current_city]
            dap = []

            while len(path) != max_days + 2:
                neighbours = [(u, v, d) for (u, v, d) in self.G.edges(current_city, data=True) if
                             d['day'] == current_day and v in to_visit]

                if neighbours:
                    current_city, price = self._select_neighbour(neighbours)
                    to_visit.remove(current_city)
                else:
                    price = (max_days + 2 - len(path)) * 10000

                path.append(current_city)
                dap.append([current_day, price])
                current_day += 1

                if not neighbours:
                    break

            paths.append(path)
            days_and_prices.append(dap)

        return paths, days_and_prices

    def _init_pheromone(self):
        last_city_from = ''
        last_city_to = ''
        for city_from, city_to in self.G.edges_iter():
            if city_from == last_city_from and city_to == last_city_to:
                continue
            for i in range(len(self.G[city_from][city_to])):
                self.G[city_from][city_to][i]['phe'] = random.uniform(self.min_phe, self.max_phe)
            last_city_from = city_from
            last_city_to = city_to

    def _evaporate(self):
        last_city_from = ''
        last_city_to = ''
        for city_from, city_to in self.G.edges_iter():
            if city_from == last_city_from and city_to == last_city_to:
                continue

            for i in range(len(self.G[city_from][city_to])):
                updated_phe = (1 - self.rho) * self.G[city_from][city_to][i]['phe'] + .00001
                if self.min_phe < updated_phe < self.max_phe:
                    self.G[city_from][city_to][i]['phe'] = updated_phe

            last_city_from = city_from
            last_city_to = city_to

    def _update_pheromone(self, paths, days_and_prices):
        if self.evaporation:
            self._evaporate()

        for path, dap in zip(paths, days_and_prices):
            phe = 1.0 * self.mu / max(self._calculate_total_price(dap), 0.00001)
            edges = zip(path[:-1], path[1:])
            for i, (city_from, city_to) in enumerate(edges):
                if self.G[city_from].get(city_to, None):
                    for j in range(len(self.G[city_from][city_to])):
                        if self.G[city_from][city_to][j]['weight'] == dap[i][1] and self.G[city_from][city_to][j][
                            'day'] == dap[i][0]:
                            # add more phe to first flights
                            if self.min_phe < (self.G[city_from][city_to][j]['phe'] + phe / (i + 1)) < self.max_phe:
                                self.G[city_from][city_to][j]['phe'] += phe / (i + 1)

    def _calculate_total_price(self, dap):
        return sum(x[1] for x in dap)

    def _select_best_path(self, days_and_prices):
        index = 0
        best_price = sys.maxsize

        for i, dap in enumerate(days_and_prices):
            price = self._calculate_total_price(dap)
            if price < best_price:
                best_price = price
                index = i

        return index, best_price

    def _format_path(self, path, dap):
        formatted_path = []
        for i, (city_from, city_to) in enumerate(zip(path[:-1], path[1:])):
            formatted_path.append(Flight(city_from, city_to, dap[i][0], dap[i][1]))
        return formatted_path

    def search(self, iterations):
        global_best_path = []
        global_dap = []
        global_best_price = sys.maxsize

        for i in range(iterations):
            if i % self.phe_reinit == 0:
                self._init_pheromone()

            paths, days_and_prices = self._construct_paths()

            self._update_pheromone(paths, days_and_prices)
            index, best_price = self._select_best_path(days_and_prices)

            if best_price < global_best_price:
                global_best_path = paths[index]
                global_dap = days_and_prices[index]
                global_best_price = best_price

        return self._format_path(global_best_path, global_dap), global_best_price
