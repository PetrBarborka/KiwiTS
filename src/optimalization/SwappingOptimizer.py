from itertools import permutations


class SwappingOptimizer:
    def __init__(self):
        pass

    def _get_path_cost(self, path):
        return sum(p.price for p in path)

    def run(self, path, dataset, swap=3, stride=1):
        path_length = len(path) + 1

        assert (3 <= swap <= path_length), '3 <= swap <= len(flights)'
        assert (1 <= stride <= path_length), '1 <= stride <= len(flights)'

        for i in range(0, path_length - swap, stride):
            path_chunk = path[i:i + swap]
            cost = self._get_path_cost(path_chunk)

            cities_to_visit = [p.city_from for p in path_chunk[1:]]

            for cities_perm in permutations(cities_to_visit):
                current_city = path_chunk[0].city_from
                current_day = path_chunk[0].day

                new_path = []
                try:
                    for city in cities_perm:
                        flight = \
                        dataset.get_flights(current_city, current_day, cities_to_visit=[city], sort_by_price=True)[0]

                        current_city = flight.city_to
                        current_day += 1

                        new_path.append(flight)

                    last_flight = \
                    dataset.get_flights(current_city, current_day, cities_to_visit=[path_chunk[-1].city_to],
                                        sort_by_price=True)[0]
                    new_path.append(last_flight)

                    new_cost = self._get_path_cost(new_path)
                    if new_cost < cost:
                        cost = new_cost
                        path_chunk = new_path[:]
                except IndexError:
                    break

            path[i:i + swap] = path_chunk

        return path
