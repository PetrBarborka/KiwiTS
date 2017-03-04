cdef class CFlight:
    """ Class representing one flight """

    cdef int int_id
    cdef int day
    cdef int price
    cdef city_from
    cdef city_to

    def __cinit__(self, city_from, city_to, int day, int price, int int_id=-1):
        self.int_id = int_id
        self.city_from = city_from
        self.city_to = city_to
        self.day = day
        self.price = price

    property int_id:
        def __get__(self):
            return self.int_id
        def __set__(self, int_id):
            self.int_id = int_id

    property city_from:
        def __get__(self):
            return self.city_from
        def __set__(self, city_from):
            self.city_from = city_from

    property city_to:
        def __get__(self):
            return self.city_to
        def __set__(self, city_to):
            self.city_to = city_to
            
    property day:
        def __get__(self):
            return self.day
        def __set__(self, day):
            self.day = day

    property price:
        def __get__(self):
            return self.price
        def __set__(self, price):
            self.price = price

    def __str__(self):
        return 'id: {}, {} {} {} {}'.format(self.int_id,
                                            self.city_from,
                                            self.city_to,
                                            self.day,
                                            self.price)

    def __repr__(self):
        return '<Flight: {}>'.format(str(self))

    def __richcmp__(x, y, op):
        if op == 2:#Py_EQ -> ==
            return x.__is_equal(y)
        if op == 3:#Py_NE -> !=
            return not x.__is_equal(y)
        else:
            assert False

    def __is_equal(self, other): #private helper method
        return  self.city_from == other.city_from  and \
                self.city_to == other.city_to and \
                self.day == other.day and \
                self.price == other.price
