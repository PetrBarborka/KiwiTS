from heapq import heappush, heappop


class ShortestPath:
    def __init__(self):
        pass

    def _is_possible_flight(self, flight, starting_city, last_day):
        # allow only flights from the starting city on first day of the trip
        is_first_day_flight = flight.city_from == starting_city and flight.day == 0

        # allow only flights to the starting city on the last day of the trip
        is_last_day_flight = flight.city_to == starting_city and flight.day == last_day

        # do not allow flights to the starting city during the trip
        is_midtrip_flight = flight.city_to != starting_city and flight.day != 0 and flight.day != last_day

        # do not allow flights from and back to the same city - should not be in dataset, just making sure
        is_same_city = flight.city_from == flight.city_to

        return (is_first_day_flight or is_last_day_flight or is_midtrip_flight) and not is_same_city

    def _single_source_dijkstra(self, dataset, starting_city, days):
        heap = []
        prices = {}
        paths = {(starting_city, 0): []}
        visited = {(starting_city, 0): []}

        heappush(heap, (starting_city, 0, 0))

        while heap:
            (city_from, current_day, price) = heappop(heap)
            # print('-' * 45)
            # print('|   City: {}   |   Day: {}   |   Price: {}   |'.format(city_from, current_day, price))
            # print('-' * 45)
            prices[(city_from, current_day)] = price

            if city_from == starting_city and current_day != 0:
                break

            # print('Possible flights:')
            flights_to_take = {}
            for flight in dataset.get_flights(city_from, current_day):
                if self._is_possible_flight(flight, starting_city, days) and flight.city_to:
                    # print('  ', flight)
                    city_to = flight.city_to
                    # take care of multiple flights to same destination with different prices
                    if flights_to_take.get(city_to, None):
                        if flight.price < flights_to_take[city_to].price:
                            flights_to_take[city_to] = flight

                    else:
                        flights_to_take[city_to] = flight

            # print('Cheapest flights:')
            for flight in flights_to_take.values():
                # print('  ', flight)
                price = prices[(city_from, current_day)] + flight.price
                next_day = current_day + 1
                city_to = flight.city_to

                last_flight_key = (city_from, current_day)
                next_flight_key = (city_to, next_day)

                if (next_flight_key not in prices or price < prices[next_flight_key]) and city_to not in visited[
                    last_flight_key]:
                    paths[next_flight_key] = paths[last_flight_key] + [flight]
                    visited[next_flight_key] = visited[last_flight_key] + [city_to]
                    heappush(heap, (city_to, next_day, price))

                    # print('Seen:')
                    # for k, v in seen.items():
                    #     print('  ', k, v)
                    # print('Paths:')
                    # for k, v in paths.items():
                    #     print('  ', k, v)
                    # print('Visited:')
                    # for k, v in visited.items():
                    #     print('  ', k, v)
                    # print('Heap:')
                    # print('  ', heap)

        return paths, prices

    def search(self, dataset):
        starting_city = dataset.get_starting_city()
        last_day = len(dataset)

        paths, prices = self._single_source_dijkstra(dataset, starting_city, last_day - 1)
        return paths[(starting_city, last_day)], prices[(starting_city, last_day)]
