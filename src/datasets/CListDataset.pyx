import copy

from CFlight import CFlight

cdef class CListDataset:
    cdef dataset
    cdef flights
    cdef int next_flight_id
    cdef int next_city_id
    cdef starting_city
    cdef cities
    cdef cities_id_map

    def __cinit__(self):
        self.dataset = None
        self.flights = []
        self.next_flight_id = 0
        self.next_city_id = 0
        self.starting_city = None
        self.cities = None
        self.cities_id_map = dict()

    def copy(self):
        new = CListDataset()
        new.dataset = copy.deepcopy(self.dataset)
        new.flights = copy.deepcopy(self.flights)
        new.next_flight_id = self.next_flight_id
        new.next_city_id = self.next_city_id
        new.starting_city = self.starting_city
        new.cities = list(self.cities)
        for k, v in self.cities_id_map.items():
            new.cities_id_map[k] = v

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
    property next_flight_id:
        def __get__(self):
            return self.next_flight_id
        def __set__(self, p):
            self.next_flight_id = p
    property next_city_id:
        def __get__(self):
            return self.next_city_id
        def __set__(self, p):
            self.next_city_id = p
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
    property cities_id_map:
        def __get__(self):
            return self.cities_id_map
        def __set__(self, p):
            self.cities_id_map = p

    def __len__(self):
        return len(self.cities)

    def __repr__(self):
        return self.starting_city + repr(self.dataset)

    def load_data(self, path):
        with open(path, 'r') as fr:
            self.starting_city = fr.readline().rstrip()
            lines = fr.readlines()
        list(map(lambda line: self._build_cities_id_map(line.split(' ')), lines))
        self.cities = list(self.cities_id_map.keys())
        self.dataset = [[list() for day in self.cities] for city in self.cities]
        list(map(lambda line: self._process_one_line(line.split(' ')), lines))

    def _build_cities_id_map(self, splt_line):
        if splt_line[0] not in self.cities_id_map:
            self.cities_id_map[splt_line[0]] = self.next_city_id
            self.next_city_id += 1

    def _process_one_line(self, splt_line):
        city_from = splt_line[0]
        city_to = splt_line[1]
        day = int(splt_line[2])
        price = int(splt_line[3])
        flight = CFlight(city_from, city_to, day, price, self.next_flight_id)
        self.flights.append(flight)
        self.next_flight_id += 1
        self.dataset[self.cities_id_map[city_from]][day].append(flight)

    def get_starting_city(self):
        return self.starting_city

    def get_flight_by_id(self, int_id):
        return self.flights[int_id]

    def get_flights(self, airport_code, day, cities_to_visit=None, sort_by_price=None):
        possibilities = self.dataset[self.cities_id_map[airport_code]][day]
        if sort_by_price is not None:
            possibilities = sorted(possibilities, key=lambda p: p.price)
        if cities_to_visit is None:
            return possibilities
        else:
            return [f for f in possibilities if f.city_to in cities_to_visit]
