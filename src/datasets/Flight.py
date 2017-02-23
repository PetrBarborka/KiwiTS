class Flight:
    """ Class representing one flight """
    def __init__(self, city_from, city_to, day, price):
        self.city_from = city_from
        self.city_to = city_to
        self.day = day
        self.price = price

    def __str__(self):
        return '{} {} {} {}'.format(self.city_from, self.city_to, self.day, self.price)

    def __repr__(self):
        return '<Flight: {}>'.format(str(self))

    def __eq__(self, other):
        return  self.city_from == other.city_from and \
                self.city_to == other.city_to and \
                self.day == other.day and \
                self.price == other.price