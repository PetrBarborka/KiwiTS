import random
import copy


class HenryGenerator:
    def __init__(self, airports=3, name_length=3, price_min=10, price_max=200,
        flights_per_airport_min=1, flights_per_airport_max=5):
        self.characters = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
        'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.n_of_airports = airports
        self.name_length = name_length
        self.price_min = price_min
        self.price_max = price_max
        self.flights_per_airport_min = flights_per_airport_min
        self.flights_per_airport_max = flights_per_airport_max
        self.flights = None
        self.target_flights = None
        self.starting_city = None
        self.trip_price = 0

    def _generate_airports(self, n_of_airports):
        def __generate_name():
            out = ''
            for i in range(self.name_length):
                out += self.characters[random.randint(0, len(self.characters)-1)]
            return out

        airports = list()
        for i in range(n_of_airports):
            new_name = __generate_name()
            while new_name in airports:
                new_name = __generate_name()
            airports.append(new_name)
        return airports

    def _generate_flights(self, airport_list):
        def __generate_number_of_flights():
            return random.randint(self.flights_per_airport_min, self.flights_per_airport_max)
        def __generate_price():
            return random.randint(self.price_min, self.price_max)
        def __generate_day():
            return random.randint(0, len(airport_list)-1)
        def __generate_destination(forbidden_index):
            target_airport = forbidden_index
            while target_airport == forbidden_index:
                target_airport = random.randint(0, len(airport_list)-1)
            return airport_list[target_airport]

        flights = list()
        for index, airport in enumerate(airport_list):
            for i in range(__generate_number_of_flights()):
                flights.append([
                    airport,
                    __generate_destination(index),
                    __generate_day(),
                    __generate_price()
                ])
        return flights

    def _generate_best_path(self, airport_list, random_cost=False):
        def __pop_random_from_list(lst):
            return lst.pop(random.randint(0, len(lst)-1))
        def __get_price(random_cost):
            price = 10 * random.randint(self.price_min, self.price_max) if random_cost else 0
            self.trip_price += price
            return price
        airports = copy.copy(airport_list)
        flights = list()
        flying_from = __pop_random_from_list(airports)
        while(len(airports)>0):
            flying_to = __pop_random_from_list(airports)
            flights.append([
                flying_from,
                flying_to,
                len(flights),
                __get_price(random_cost)
            ])
            flying_from = flying_to
        flights.append([
            flying_from,
            flights[0][0],
            len(flights),
            __get_price(random_cost)
        ])
        return flights

    def save_input_file(self, path=None):
        if not self.flights:
            self.generate()
        string = '{}\n'.format(self.starting_city)
        for f in self.flights:
            string += '{} {} {} {}\n'.format(*f)
        string = string[:-1]
        if path:
            with open(path, 'w') as f:
                f.write(string)
        return string

    def save_target_file(self, path=None):
        if not self.flights:
            self.generate()
        string = '{}\n'.format(self.trip_price)
        for f in self.target_flights:
            string += '{} {} {} {}\n'.format(*f)
        string = string[:-1]
        if path:
            with open(path, 'w') as f:
                f.write(string)
        return string

    def generate(self, generate_best_path=True, random_cost=False):
        airports = self._generate_airports(self.n_of_airports)
        flights = self._generate_flights(airports)
        if generate_best_path:
            best_path = self._generate_best_path(airports, random_cost)
            flights.extend(best_path)
            self.starting_city = best_path[0][0]
            self.target_flights = best_path
        else:
            self.target_flights = None
            self.starting_city = flights[random.randint(0, len(flights)-1)][0]
        flights = sorted(flights, key=lambda x: (x[0], x[2]))
        self.flights = flights
        return flights
