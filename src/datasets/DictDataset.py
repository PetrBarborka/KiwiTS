from .DatasetInterface import DatasetInterface
from .Flight import Flight

import sys


class DictDataset(DatasetInterface):
    """ Class representing dataset with dict
        dataset = { from: { day: [Flight1, Flight2, ... ] } } """

    def __init__(self):
        self.dataset = dict()
        self.flights = dict() # stores flights by IDs
        self.next_id = 0 # next ID to be assigned to a flight
        self.starting_city = None
        self.cities = []

    def __len__(self):
        return len(self.cities)

    def __repr__(self):
        return self.starting_city + repr(self.dataset)

    def load_data(self, path):
        """ See DatasetInterface """
        with open(path, 'r') as f:
            self.starting_city = f.readline().rstrip()
            lines = f.readlines()
        self._proccess_input(lines)
        self.cities = list(self.dataset.keys())

    def _proccess_input(self, lines):
        """ Proccesses input file lines to dict """
        def __add_to_dataset(from_city, to_city, day, price):
            """ Adds given flight to dataset """
            flight = Flight(from_city, to_city, day, price, self.next_id)
            self.flights[self.next_id] = flight
            self.next_id += 1
            if from_city in self.dataset:
                if day in self.dataset[from_city]:
                    self.dataset[from_city][day].append(flight)
                else:
                    self.dataset[from_city][day] = [flight]
            else:
                self.dataset[from_city] = {day:[flight]}

        for line in lines:
            l = line.split(' ') # from, to, day, price
            __add_to_dataset(l[0], l[1], int(l[2]), int(l[3]))

    def get_starting_city(self):
        """ See DatasetInterface """
        return self.starting_city

    def get_flight_by_id(self, int_id):
        return self.flights[int_id]

    def get_flights(self, airport_code, day,
                    cities_to_visit=None, sort_by_price=None):
        """ See DatasetInterface """
        possibilities = self.dataset[airport_code].get(day, list())
        if sort_by_price is not None:
            possibilities = sorted(possibilities, key=lambda p: p.price)
        if cities_to_visit is None:
            return possibilities
        else:
            return [f for f in possibilities if f.city_to in cities_to_visit]
