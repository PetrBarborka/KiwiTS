from .Flight import Flight
from .CFlight import CFlight

class DataPath:

    def __init__(self, flights=None, price=0):
        # assert len(flights) > 0
        assert type(price) is type(5)
        # assert isinstance(flights[0], Flight) or isinstance(flights[0], CFlight)

        self.flights = flights if flights is not None else []
        self.price = price

    def copy(self):
        o = DataPath()
        for f in self.flights:
            o.push_flight(f)
        return o

    def is_valid(self, partial=False):

        cities = set()

        cur = self.flights[0].city_from
        valid  = True
        for f in self.flights:
            valid = valid and f.city_from == cur
            cur = f.city_to
            cities.add(cur)

        valid = valid and len(cities) == len(self.flights)

        if partial:
            return valid
        else:
            valid = valid and self.flights[0].city_from == self.flights[-1].city_to
            return valid

    def push_flight(self, flight):
        assert type(flight.price) is type(5)
        assert isinstance(flight, Flight) or isinstance(flight, CFlight)

        self.flights.append(flight)
        self.price += flight.price

    def pop_flight(self):

        out = self.flights.pop(-1)
        self.price -= out.price

        return out

    def __str__(self):
        out = ""
        for f in self.flights:
            out += "{}".format(repr(f))
        out += " price: {}".format(self.price)
        return out

    def __repr__(self):
        return '<Path: {}>'.format(str(self))

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        assert isinstance(other, self.__class__)
        eq = True
        for i in range(len(self.flights)):
            eq = eq and self.flights[i] == other.flights[i]
        eq = eq and self.price == other.price
        return eq
