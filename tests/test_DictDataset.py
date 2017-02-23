import unittest

import sys, os
sys.path.append(os.path.realpath(".."))

class DictDatasetTest(unittest.TestCase):

    def test_cities(self):
        from src.datasets import DictDataset
        d = DictDataset()
        d.load_data('../input/3_airports_backtrace.csv')

        self.assertTrue("PRG" in d.cities )
        self.assertTrue("TXL" in d.cities )
        self.assertTrue("TXL" in d.cities )

    def test_num_flights(self):
        from src.datasets import DictDataset
        d = DictDataset()
        d.load_data('../input/3_airports_backtrace.csv')
        
        count = 0
        for ap in d.dataset:
            for day in ap:
                for flight in day:
                    count += 1
        self.assertEquals( count, 9 )

if __name__ == '__main__':
    unittest.main()
