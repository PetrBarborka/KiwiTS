import random
import copy


class HenryGenerator2:
    def __init__(self, num_airports=3, 
                 price_min=10, price_max=200,
                 flights_total=100, paths_total=1,
                 cheapest_path=False, most_expensive_path=False):

        assert paths_total > 0
        
        self.characters = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
        'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        self.n_noise_flights = flights_total - num_airports*paths_total
        self.n_of_airports = num_airports

        self.price_min = price_min
        self.price_max = price_max

        self.n_paths_total = paths_total

        self.airports = None
        self.flights = None
        self.paths = []
        self.best_path = None
        self.starting_city = None

        self.most_expensive_path = most_expensive_path
        self.cheapest_path = cheapest_path

        self.generate()

    def _generate_airports(self):
        def __generate_name():
            out = ''
            for i in range(3):
                out += self.characters[random.randint(0, len(self.characters)-1)]
            return out

        airports = list()
        for i in range(self.n_of_airports):
            new_name = __generate_name()
            while new_name in airports:
                new_name = __generate_name()
            airports.append(new_name)
        self.airports = airports
        self.starting_city = airports[0]
        return airports

    def _generate_noise_flights(self):
        def __generate_number_of_flights():
            return int (self.n_noise_flights / self.n_of_airports)
        def __generate_price():
            return random.randint(self.price_min, self.price_max)
        def __generate_day():
            return random.randint(0, len(self.airports)-1)
        def __generate_destination(forbidden_index):
            target_airport = forbidden_index
            while target_airport == forbidden_index:
                target_airport = random.randint(0, len(self.airports)-1)
            return self.airports[target_airport]

        flights = list()
        for index, airport in enumerate(self.airports):
            for i in range(__generate_number_of_flights()):
                flights.append([
                    airport,
                    __generate_destination(index),
                    __generate_day(),
                    __generate_price()
                ])
        return flights

    def _generate_path(self, cost=None):
        def __pop_random_from_list(lst):
            return lst.pop(random.randint(0, len(lst)-1))
        def __get_price(cost):
            price = random.randint(self.price_min, self.price_max) if cost is None else int(cost/self.n_of_airports)
            return price
        airports = copy.copy(self.airports)
        airports.remove(self.starting_city)
        flights = list()
        flying_from = self.starting_city
        
        total_price = 0

        while(airports):
            flying_to = __pop_random_from_list(airports)
            price = __get_price(cost)
            total_price += price
            flights.append([
                flying_from,
                flying_to,
                len(flights),
                price
            ])
            flying_from = flying_to
        price = __get_price(cost)
        flights.append([
            flying_from,
            flights[0][0],
            len(flights),
            price
        ])
        total_price += price
        return flights, total_price

    def save_input_file(self, path=None):
        string = '{}\n'.format(self.starting_city)
        for f in self.flights:
            string += '{} {} {} {}\n'.format(*f)
        string = string[:-1]
        if path:
            with open(path, 'w') as f:
                f.write(string)
        return string

    def save_target_file(self, path=None):
        string = '{}\n'.format(self.best_path[1])
        for f in self.best_path[0]:
            string += '{} {} {} {}\n'.format(*f)
        string = string[:-1]
        if path:
            with open(path, 'w') as f:
                f.write(string)
        return string

    def save_all_paths_file(self, path=None):
        string = ''
        for p in self.paths:
            string += '\n\n'
            string += '{}\n'.format(p[1])
            for f in p[0]:
                string += '{} {} {} {}\n'.format(*f)
            string = string[:-1]
            if path:
                with open(path, 'w') as f:
                    f.write(string)
        return string

    def generate(self, generate_best_path=True, random_cost=False):
        if self.cheapest_path and self.most_expensive_path:
            assert self.n_paths_total > 1, "you need at least 2 paths if you want both \
                                     cheapest and most expensive"
        self._generate_airports()
        self.flights = self._generate_noise_flights()
        paths_to_make = self.n_paths_total
        if self.most_expensive_path:
            path = self._generate_path(cost=(self.price_max * len(self.airports) + len(self.airports)))
            self.paths.append(path)
            self.flights.extend(path[0])
            paths_to_make -= 1
        if self.cheapest_path:
            path = self._generate_path(cost=0)
            self.paths.append(path)
            self.flights.extend(path[0])
            paths_to_make -= 1
        for i in range(paths_to_make):
            path = self._generate_path()
            self.paths.append(path)
            self.flights.extend(path[0])

        self.flights = sorted(self.flights, key=lambda x: (x[0], x[2]))
        self.paths = sorted(self.paths, key=lambda x: x[1]) 
        self.best_path = self.paths[0]

        return self.flights, self.paths, self.best_path
