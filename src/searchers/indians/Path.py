import copy


class Path:
    def __init__(self, starting_city, total_cities):
        self.starting_city = starting_city
        self.total_cities = total_cities
        self.cities_dict = {starting_city:1}
        self.flights = []
        self.current_city = starting_city
        self.price = 0

    def __repr__(self):
        return '<Path: price: {}, flights:{}>'.format(self.price, str(self.flights))

    def to_string(self, dataset):
        str_out = '<Path: price {}\n'.format(self.price)
        for f in self.flights:
            str_out += str(dataset.get_flight_by_id(f)) + '\n'
        str_out += '>'
        return str_out

    def possible_flight(self, flight):
        # is returning flight and its time to return
        if flight.city_to == self.starting_city and len(self.flights) + 1 == self.total_cities:
            return True
        # the destination has not yet been visited
        else:
            return not flight.city_to in self.cities_dict

    def is_valid(self):
        # gets set to 0 when returning flight is appended
        returned_home = self.cities_dict[self.starting_city] == 0
        all_cities_visited = len(self.cities_dict) == self.total_cities

        # the path is complete
        return all_cities_visited and returned_home

    def add_to_path(self, flight):
        self.cities_dict[flight.city_to] = 0
        self.price += flight.price
        self.flights.append(flight.int_id)
        self.current_city = flight.city_to

    def get_current_city(self):
        return self.current_city

    def get_copy(self):
        p = Path(self.starting_city, self.total_cities)
        p.cities_dict = copy.copy(self.cities_dict)
        p.flights = copy.copy(self.flights)
        p.price = self.price
        return p
