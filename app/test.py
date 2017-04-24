from subprocess import call

"""A short script to test whether the './run'
   deployment wrapper works. 
"""

# This is a path to the data provided by kiwi.
# If you don't have it, go to ../../kiwisources and do
# "git clone https://github.com/kiwicom/travelling-salesman.git"
repo = "../../kiwisources/travelling-salesman/"
# repo = "/repo/"

# n = [5, 10, 15, 20, 30, 40, 50, 60, 70, 100, 200, 300]
n = [5, 10]

files = ["{}real_data/data_{}.txt".format(repo, i) for i in n]

for f in files:
    call( "cat {} | ./run".format(f), shell=True )
