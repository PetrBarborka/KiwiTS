# encoding: utf-8
# cython: profile=True
# filename: CMatrixDataset.pyx

from .DatasetInterface import DatasetInterface
from .CFlight import CFlight

import numpy as np
cimport numpy as np

import csv

cdef class CMatrixDataset:
    """ Class representing dataset with dict
        dataset = { from: { day: [Flight1, Flight2, ... ] } } """

    cdef public np.ndarray dataset
    cdef public int next_id  # next ID to be assigned to a flight
    cdef public starting_city
    cdef public cities
    cdef public city_name_to_id
    cdef public city_id_to_name

    def __init__(self):
        self.dataset = None
        self.next_id = 0  # next ID to be assigned to a flight
        self.starting_city = None
        self.cities = list()
        self.city_name_to_id = {}
        self.city_id_to_name = {}

    def __len__(self):
        return len(self.cities)

    def __repr__(self):
        return self.starting_city + repr(self.dataset)

    def load_data(self, path):
        """ See DatasetInterface """
        assert self.dataset is None

        def fast_split_line(input_line):
            s = input_line[8:].split(' ')
            return [input_line[:3], input_line[4:7],
                    s[0], s[1]]

        def stripline(l):
            nrs = l[8:].split(b' ')
            return  [  str(l[0:3])[2:5], 
                    str(l[4:7])[2:5],
                    int(nrs[0]),
                    int(nrs[1]),
                    ]

        reader = None
        with open(path, 'r') as f:
            self.starting_city = f.readline().rstrip()

            self.cities.append(self.starting_city)
            self.city_name_to_id[self.starting_city] = 0
            self.city_id_to_name[0] = self.starting_city

            self.dataset = np.empty((len(open(path).readlines())-1, 4), dtype=np.int)
            reader = csv.reader(f, delimiter=" ")

            # for l in lines:
            for l in reader:

                # splt_line = l.split(b' ')
                # splt_line = stripline(l)
                splt_line = l
                
                from_name = splt_line[0]
                try:
                    city_from_id = self.city_name_to_id[from_name]
                except KeyError:
                    city_from_id = len(self.cities)
                    self.cities.append(from_name)

                    self.city_name_to_id[from_name] = city_from_id
                    self.city_id_to_name[city_from_id] = from_name

                to_name = splt_line[1]
                try:
                    city_to_id = self.city_name_to_id[to_name]
                except KeyError:
                    city_to_id = len(self.cities)
                    self.cities.append(to_name)

                    self.city_name_to_id[to_name] = city_to_id
                    self.city_id_to_name[city_to_id] = to_name

                self.dataset[self.next_id, 0] = city_from_id
                self.dataset[self.next_id, 1] = city_to_id
                self.dataset[self.next_id, 2] = splt_line[2]
                self.dataset[self.next_id, 3] = splt_line[3]

                self.next_id += 1


    def get_starting_city(self, by_id=None):
        """ See DatasetInterface """
        if by_id:
            return 0
        else:
            return self.starting_city

    def get_flight_by_id(self,int int_id):
        src = self.cities[self.dataset[int_id, 0]]
        dest = self.cities[self.dataset[int_id, 1]]
        f = CFlight(src, dest, self.dataset[int_id, 2], self.dataset[int_id, 3], int_id=int_id)
        return f

    def get_flights(self, airport_code, int day,
                    cities_to_visit=None, sort_by_price=None):
        """ Construct and return Fligths """
        d = self.dataset

        city_from_id = self.cities.index(airport_code)

        ids = np.where( (d[:,0] == city_from_id) & (d[:,2] == day) )
        p = d[ids]
        possibilities = []
        for i,f in zip(ids[0], p):
            possibilities.append( CFlight(self.cities[f[0]], self.cities[f[1]], \
                                          day, f[3], int_id=i) )

        if sort_by_price is not None:
            possibilities = sorted(possibilities, key=lambda p: p.price)
        if cities_to_visit is None:
            return possibilities
        else:
            return [f for f in possibilities if f.city_to in cities_to_visit]

    def get_flights_ids(self, int from_id, int day, cities_to_visit_ids=None,
                        sort_by_price=None):
        """ Return flights as arrays if [from_id, to_id, day, price] """
        d = self.dataset
        # print( "dataset: {}".format(d) )
        possibilities = d[(d[:,0] == from_id) & (d[:,2] == day)]

        if sort_by_price is not None:
            possibilities = possibilities[possibilities[:,3].argsort()]
        if cities_to_visit_ids is None:
            return possibilities
        else:
            ri = np.in1d(possibilities[:,1], cities_to_visit_ids)
            return possibilities[ri,:]
