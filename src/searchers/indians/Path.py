import copy


class Path:
    def __init__(self, starting_city, total_cities):
        self.starting_city = starting_city
        self.total_cities = total_cities
        self.cities_dict = {starting_city:1}
        self.flights = []
        self.price = 0

    def __repr__(self):
        return '<Path: price: {}, flights:{}>'.format(self.price, str(self.flights))

    def possible_flight(self, flight):
        if flight.city_to == self.starting_city and len(self.flights) + 1 == self.total_cities:
            return True
        else:
            return not flight.city_to in self.cities_dict

    def is_valid(self):
        bool_a = self.cities_dict[self.starting_city] == 0
        bool_b = len(self.cities_dict) == self.total_cities
        return bool_a and bool_b

    def add_to_path(self, flight):
        self.cities_dict[flight.city_to] = 0
        self.price += flight.price
        self.flights.append(flight)

    def get_current_city(self):
        return self.flights[-1].city_to

    def get_copy(self):
        p = Path(self.starting_city, self.total_cities)
        p.cities_dict = copy.copy(self.cities_dict)
        p.flights = copy.copy(self.flights)
        p.price = self.price
        return p
