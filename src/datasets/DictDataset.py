from DatasetInterface import DatasetInterface
from Flight import Flight

import sys


class DictDataset(DatasetInterface):
    """ Class representing dataset with dict """
    def __init__(self):
        self.dataset = dict()
        self.starting_city = None

    def load_data(self, path):
        """ See DatasetInterface """
        with open(path, 'r') as f:
            lines = f.readlines()
        self.starting_city = lines[0]
        self._proccess_input(lines[1:])

    def _proccess_input(self, lines):
        """ Proccesses input file lines to dict """
        def __add_to_dataset(from_city, to_city, day, price):
            """ Adds give flight to dataset """
            flight = Flight(from_city, to_city, day, price)
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

    def get_flights(self, airport_code, day):
        """ See DatasetInterface """
        return self.dataset[airport_code].get(day, None)
