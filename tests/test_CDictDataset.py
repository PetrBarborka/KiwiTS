import unittest

import sys, os
sys.path.append(os.path.realpath(".."))

class DictDatasetTest(unittest.TestCase):

    def test_cities(self):
        from src.datasets.CDictDataset import CDictDataset
        d = CDictDataset()
        d.load_data('../input/3_airports_backtrace.csv')

        self.assertTrue("PRG" in d.cities )
        self.assertTrue("TXL" in d.cities )
        self.assertTrue("TXL" in d.cities )

    def test_num_flights(self):
        from src.datasets.CDictDataset import CDictDataset
        d = CDictDataset()
        d.load_data('../input/3_airports_backtrace.csv')
        
        count = 0
        for ap in d.dataset:
            for day in d.dataset[ap]:
                for flight in d.dataset[ap][day]:
                    count += 1
        self.assertEquals( count, 9 )

if __name__ == '__main__':
    unittest.main()
