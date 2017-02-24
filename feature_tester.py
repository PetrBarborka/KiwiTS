def generate_flights():
    from src.generators import HenryGenerator

    generator = HenryGenerator(
        name_length = 3,
        flights_per_airport_min = 500,
        flights_per_airport_max = 1000,
        airports = 500
    )
    generator.generate()

    generator.save_input_file('input/500_airports_input.csv')
    #print('----')
    generator.save_target_file('input/500_airports_target.csv')

def load_data():
    from src.datasets import DictDataset
    d = DictDataset()
    d.load_data('input/500_airports_input.csv')
    # d.load_data('input/3_airports_backtrace.csv')
    return d

#generate_flights()
#exit()

dataset = load_data()

from src.searchers import Tribe
t = Tribe()
t.search(dataset)
exit()

from src.searchers import BackTracker
b = BackTracker()

r = b.search(dataset)
if r:
    print( dataset.starting_city )
    for f in r:
        print( f )
