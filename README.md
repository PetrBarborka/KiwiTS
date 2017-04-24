# Kiwi Travelling Salesman competition submission

This was our shot at the [travelling salesman
competition](https://github.com/kiwicom/travelling-salesman) hosted by Kiwi.com.

## Outline
We were given a dataset containing data about flights that go from a airport 1 to
airport 2 at a given day for a given price and a starting airport. We were 
supposed to find a full cycle that has one flight every day and visits all 
the airports in the dataset.

We tried various methods of loading and storing of the data as well as many
methods to search for the cycle. In the end, we went for dictionary dataset and
a simple backtracking algorithm, which proved the most efficient. 

Python turned out not to be the greatest tool to do that, because we failed to
even load the biggest dataset in the timeout of 30s. However, we did provide a
working solution that was able to compete on the other, smaller datasets.

Out of the circa 300 teams enlisted, about 70 provided a working solution and
we placed somewhere around 30th place.

## Running

You'll find the 'run' bash wrapper and a simple test script in the 'app' folder.

To run the code, you will need 

+ python 3, numpy and Cython, both of which can be
installed with pip3 (might require sudo). 
+ compile Cython components: go to src/datasets and src/searchers and run
  build.sh in both places.

Benchmarking and some other scripts may require the kiwi repo to be cloned and
files unpacked into kiwisources/ 
(git clone https://github.com/kiwicom/travelling-salesman.git),
which is kinda big and you don't need it for the app/test.py testscript.

## Exploration

I have added readmes to most of the subfolders to give a basic outline of what
is where.

If you want to only check what we actually used in the end, look into:
+ app/
+ run_async.py
+ src/datasets/CDictDataset.pyx
+ src/datasets/CFlight.pyx
+ src/searchers/CAsyncBackTracker.pyx
