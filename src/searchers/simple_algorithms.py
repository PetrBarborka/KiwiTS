import numpy as np

price = lambda x: float(np.asscalar(x[:,3]))

import sys, os
sys.path.append(os.path.realpath(".."))

def getPossibilities(data, ap_from, cities_to_visit, start_day):
    """ Where can you go from given airport 
        at given day sorted by price"""
    # row = [ from, to, day, price ]

    #starts from ap_from
    startok = (data[:,0] == ap_from).any(axis=1)
    #goes to any of cities_to_visit
    endok = (data[:,1] == cities_to_visit).any(axis=1)
    stripped_data = data[np.where(np.vstack((startok, endok)).T.all(axis=1))]
    #departing on start_day or later
    possibilities = stripped_data[np.where(stripped_data[:,2].astype(int) >= start_day)[0]]

    stripped_data = sorted(possibilities, key=price)
    stripped_data = np.asmatrix(np.asarray(stripped_data))

    return stripped_data

def NN(data, cities_to_visit):
    """greedy algorithm""" 

    #filter out data for relevant airports:
    startok = (data[:,0] == cities_to_visit).any(axis=1)
    endok = (data[:,1] == cities_to_visit).any(axis=1)
    stripped_data = data[np.where(np.vstack((startok, endok)).T.all(axis=1))]
    #sort by price
    stripped_data = sorted(stripped_data, key=price)
    stripped_data = np.asmatrix(np.asarray(stripped_data))

    # select the cheapest flight from any to any
    cur_flight = np.asarray(stripped_data[0,:])[0]
    trip = [cur_flight]

    start_ap = cur_flight[0]

    cities_to_visit.remove(cur_flight[0])
    cities_to_visit.remove(cur_flight[1])

    cur_day = int(trip[0][2])
    cur_ap = trip[0][1]

    while( cities_to_visit ):
        pos = getPossibilities(stripped_data, cur_ap, cities_to_visit, cur_day+1)
        if pos.shape[0] == 0 or pos.shape[1] == 0:
            return "Failed to find cycle", trip

        cur_flight = np.asarray(pos[0,:])[0]
        trip.append(cur_flight)
        cur_ap = cur_flight[1]
        cur_day = int(cur_flight[2])

        cities_to_visit.remove(cur_ap)

    cities_to_visit = [start_ap]
    pos = getPossibilities(stripped_data, cur_ap, cities_to_visit, cur_day+1)
    if pos.shape[0] == 0 or pos.shape[1] == 0:
        return "Failed to find cycle", trip

    cur_flight = np.asarray(pos[0,:])[0]
    trip.append(cur_flight)

    return trip


if __name__ == "__main__":

    import iotools
    from pprint import PrettyPrinter

    all_cities = ["PRG", "BCN", "TXL", "JFK", "CDG", "ORL", "SXT"]
    some_cities = ["PRG", "BCN", "JFK"]
    # data = generateData( cities, 1000, 10)
    data = iotools.readcsv("Data1.csv")

    pp = PrettyPrinter()
    pp.pprint(NN(data, all_cities))
    # # savecsv(data, "Data1.csv")
