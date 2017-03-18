from DatasetInterface import DatasetInterface
from Flight import Flight
from CFlight import CFlight

from copy import deepcopy

import sys, os

cdef class CDictDataset:
    """ Class representing dataset with dict
        dataset = { from: { day: [Flight1, Flight2, ... ] } } """

    cdef dataset
    cdef flights
    cdef int next_id
    cdef starting_city
    cdef cities

    def __cinit__(self):
        self.dataset = dict()
        self.flights = dict()  # stores flights by IDs
        self.next_id = 0  # next ID to be assigned to a flight
        self.starting_city = None
        self.cities = []

    def copy(self):
        o = CDictDataset()
        o.dataset = {}
        for k, v in self.dataset.items():
            o.dataset[k] = v
        o.flights = {}
        for k, v in self.flights.items():
            o.flights[k] = v
        o.next_id = self.next_id
        o.starting_city = self.starting_city
        for c in self.cities:
            o.cities.append(c)
        return o

    property dataset:
        def __get__(self):
            return self.dataset
        def __set__(self, p):
            self.dataset = p
    property flights:
        def __get__(self):
            return self.flights
        def __set__(self, p):
            self.flights = p
    property next_id:
        def __get__(self):
            return self.next_id
        def __set__(self, p):
            self.next_id = p
    property starting_city:
        def __get__(self):
            return self.starting_city
        def __set__(self, p):
            self.starting_city = p
    property cities:
        def __get__(self):
            return self.cities
        def __set__(self, p):
            self.cities = p

    def __len__(self):
            return len(self.cities)

    def __repr__(self):
            return self.starting_city + repr(self.dataset)

    def load_data(self, path=None, stdin=False):
        """ See DatasetInterface """
        lines = None
        if stdin:
            # data_in = sys.stdin.read().split('\n')[:-1]
            data_in = os.read(0, int(4e8))
            data_in = data_in.split(b'\n')[:-1]
            self.starting_city = data_in[0]
            lines = data_in[1:]
            list(map(lambda line: self._process_one_line(line.decode("latin-1").split(' ')), lines))
        else:
            with open(path, 'r') as f:
                self.starting_city = f.readline().rstrip()
                lines = f.readlines()
            list(map(lambda line: self._process_one_line(line.split(' ')), lines))
        self.cities = list(self.dataset.keys())

    def _process_one_line(self, splt_line):
        """ Processes one line of csv file """
        flight = CFlight(splt_line[0], splt_line[1],
                        int(splt_line[2]), int(splt_line[3]),
                        self.next_id)
        self.flights[self.next_id] = flight
        self.next_id += 1

        try: 
            self.dataset[flight.city_from][flight.day].append(flight)
        except: 
            try:
                self.dataset[flight.city_from][flight.day] = [flight]
            except:
                self.dataset[flight.city_from] = {flight.day: [flight]}

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
