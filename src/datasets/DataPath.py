from .Flight import Flight
from .CFlight import CFlight

class DataPath:

    def __init__(self, flights, price):
        assert len(flights) > 0
        assert type(price) is type(5)
        assert isinstance(flights[0], Flight) or isinstance(flights[0], CFlight)

        self.flights = flights
        self.price = price

    def is_valid(self):

        cities = set()

        cur = self.flights[0].city_from
        valid = self.flights[-1].city_to == cur
        for f in self.flights:
            valid = valid and f.city_from == cur
            cur = f.city_to
            cities.add(cur)

        valid = valid and self.flights[0].city_from == self.flights[-1].city_to

        valid = valid and len(cities) == len(self.flights)

        return valid

    def __str__(self):
        out = ""
        for f in self.flights:
            out += "{}".format(repr(f))
        out += " price: {}".format(self.price)
        return out

    def __repr__(self):
        return '<Path: {}>'.format(str(self))

    def __eq__(self, other):
        assert isinstance(other, self.__class__)
        eq = True
        for i in range(len(self.flights)):
            eq = eq and self.flights[i] == other.flights[i]
        eq = eq and self.price == other.price
        return eq
