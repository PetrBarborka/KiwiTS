
import csv
from random import randint
from copy import deepcopy
import numpy as np

def generateData( cities, total_connections, num_days):
    # cities = ["PRG", "BCN", "TXL"]

    data = []

    for t in range(total_connections):
        cur_cities = deepcopy(cities)

        i = randint(0, len(cur_cities)-1)
        ap_from = cur_cities.pop(i)

        i = randint(0, len(cur_cities)-1)
        ap_to = cur_cities.pop(i)

        # row = [ from, to, day, price ] 
        data.append([ap_from, ap_to, randint(1, num_days), randint(1, 20)])
    
    return np.matrix(data)

def savecsv(data, filename):
    np.savetxt(filename, data, delimiter=",", fmt="%s")

def readcsv(filename):
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return np.matrix(data)

if __name__ == "__main__":

    from pprint import PrettyPrinter

    cities = ["PRG", "BCN", "TXL", "JFK", "CDG", "ORL", "SXT"]

    data = generateData( cities, 1000, 10)

    pp = PrettyPrinter()
    pp.pprint(data)
    # savecsv(data, "Data1.csv")

    savecsv(data, "testfile.csv") 
    pp.pprint(readcsv("testfile.csv"))
