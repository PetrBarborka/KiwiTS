from src.datasets import Flight


class GraphBackTracker:
    def __init__(self, G):
        self.G = G
        self.start_city = G.graph['start_city']

    def search(self):
        to_visit = self.G.nodes()

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
                best_flight = min(possible_flights, key=lambda d: d[2]['weight'])

                cost += best_flight[2]['weight']
                current_city = best_flight[1]
                current_day += 1

                to_visit.remove(current_city)
                path.append(Flight(best_flight[0], best_flight[1], best_flight[2]['day'], best_flight[2]['weight']))
            else:
                # remove last flight from path
                if path:
                    last_flight = path.pop(-1)
                else:
                     return cost, path
                to_visit.append(current_city)

                cost -= last_flight.price
                current_city = last_flight.city_from
                current_day -= 1

                tabu[(last_flight.city_from, last_flight.city_to, last_flight.day, last_flight.price)] = 1

        return cost, path
