import sys, os
sys.path.append(os.path.realpath(".."))

from src.datasets import CDictDataset

d = CDictDataset()
d.load_data(stdin=True)

# print( d.dataset )
print( d.cities )
print(len(d.cities) )
print( d.starting_city )
