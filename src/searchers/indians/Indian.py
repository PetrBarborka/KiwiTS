import copy
from multiprocessing import Process

from .Path import Path


class Indian:
    def __init__(self, tribe, dataset, path=None, day=0):
        self.tribe = tribe
        self.dataset = dataset
        self.day = day
        self.path = path

    def start_as_chief(self):
        self.path = Path(self.dataset.get_starting_city(), len(self.dataset))
        flights = self.dataset.get_flights(self.dataset.get_starting_city(), self.day)
        self._cycle_flights(flights)

    def go(self, flight):
        self.path.add_to_path(flight)
        flights = self.dataset.get_flights(self.path.get_current_city(), self.day)
        self._cycle_flights(flights)
        if self.path.is_valid():
            self.tribe.compare_path(self.path)

    def _cycle_flights(self, flights):
        for f in flights:
            if not f.day == self.day or not self.path.possible_flight(f):
                # this should technically never happen
                continue
            path = self.path.get_copy()
            i = Indian(self.tribe, self.dataset, path, self.day+1)
            i.go(f)
