def generate_flights():
    from src.generators import HenryGenerator

    generator = HenryGenerator(
        name_length = 3,
        flights_per_airport_min = 2,
        flights_per_airport_max = 5,
        airports = 3
    )
    generator.generate()

    print(generator.save_input_file('input/3_airports_input.csv'))
    print('----')
    print(generator.save_target_file('input/3_airports_target.csv'))

def load_data():
    from src.datasets import DictDataset
    d = DictDataset()
    # d.load_data('input/3_airports_input.csv')
    d.load_data('input/3_airports_backtrace.csv')
    return d

#generate_flights()

dataset = load_data()

from src.searchers import BackTracker
b = BackTracker()

r = b.search(dataset)
if r:
    print( dataset.starting_city )
    for f in r:
        print( f )
