import multiprocessing as mp

from timeit import default_timer as timer

from src.datasets import DictDataset
from src.searchers import BackTracker
from src.searchers import ShortestPath
from src.searchers import Tribe


class AsyncManager:
    def __init__(self, dataset, searchers):
        self.dataset = dataset
        self.searchers = searchers

    def search_async(self):
        pool = mp.Pool()
        for s in self.searchers:
            pool.apply_async(self.search, args=(s, self.dataset,), callback=lambda x: self.log_result(x[0], x[1], x[2]))
        pool.close()
        pool.join()

    def search(self, searcher, dataset):
        start = timer()
        path = searcher.search(dataset)
        end = timer()

        searcher_name = searcher.__class__.__name__
        time_taken = end - start

        return searcher_name, time_taken, path

    def log_result(self, searcher_name, time_taken, path):
        cost = sum(p.price for p in path)
        print('-' * 100)
        print('Search complete:')
        print('\t{:15}{}'.format('Searcher:', searcher_name))
        print('\t{:15}{}s'.format('Run time:', round(time_taken, 5)))
        print('\t{:15}{}'.format('Cost:', cost))
        print('\t{:15}{}'.format('Path:', path))


if __name__ == '__main__':
    d = DictDataset()
    d.load_data('benchmark/benchmarkdata/300_ap_1500000_total_random_input')

    bt = BackTracker()
    sp = ShortestPath()
    t = Tribe()

    AsyncManager(d, [bt, sp, t]).search_async()
