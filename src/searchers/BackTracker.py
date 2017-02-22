class BackTracker:
    def __init__(self):
        pass

    def search(self, dataset):
        start = dataset.get_starting_city()
        flights = [start]
        day = 0

        for f in dataset.get_flights(flights[-1], day):
            print(f)
