from .Indian import Indian


class Tribe:
    def __init__(self):
        self.indians = dict()
        self.next_id = 0
        self.best_path = None
        self.best_price = None

        self.indians = list()

    def add_to_tribe(self, indian):
        self.indians.insert(0, indian)

    def compare_path(self, path):
        if not self.best_price or self.best_price > path.price:
            self.best_price = path.price
            self.best_path = path
            # print("Best price changed!")

    def search(self, dataset):
        indian = Indian(self, dataset)
        indian.start_as_chief()
        # print(self.best_path.to_string(dataset))
        return [dataset.get_flight_by_id(flt) for flt in self.best_path.flights]
