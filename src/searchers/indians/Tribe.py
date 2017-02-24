from .Indian import Indian


class Tribe:
    def __init__(self):
        self.indians = []
        self.best_path = None

    def append(self, indian):
        self.indians.append(indian)

    def search(self, dataset):
        indian = Indian(self, dataset)
        self.append(indian)
        indian.start_as_chief()
        print(self.best_path)
